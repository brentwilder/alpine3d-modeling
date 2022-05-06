# Compute snotel grids for correcting NLDAS precip
# Brent Wilder
# 05/05/2022

# Cleaned snotel data from the following paper:
# https://www.pnnl.gov/data-products 

# Import libraries
from datetime import datetime, timedelta
import pandas as pd
import geopandas as gpd
import gdal
import xarray as xr

import os
import shutil

# Set initial bounds of study****
ulx = -117
uly = 45
lrx = -114
lry = 43

# for each txt file in snotel...
list_of_dataframes = []
for file in os.listdir('./snotel'):
    filename = os.fsdecode(file)
    if filename.endswith('.txt'):
        
        # get the lat, lon from the filename
        lat = filename[5:13]
        lon = filename[14:24]
        
        # load the filename into pandas dataframe
        df = pd.read_csv('./snotel/'+filename, sep='\s{1,}', names=['Year','Month','Day','Precip','MaxT','MinT','MeanT','SWE'], header=None, engine='python')
        
        # convert to date column
        df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
        
        # convert to mm (base data is inches)
        df[filename] = 25.4 * df['Precip'] 
        
        # drop all the other data
        df = df.drop(columns=['Year', 'Month','Day','MaxT','MinT','MeanT','SWE','Precip'])
        
        # drop data prior to October 1 1981 for study****
        df = df[~(df['Date'] < '1981-10-01')]
        df['Date'] = df['Date'].dt.strftime('d_%Y%m%d')

        # Transpose
        df = df.set_index('Date')
        df = df.T

        # set lat and lon
        df['Lat'], df['Lon'] = lat , lon

        # append to list
        list_of_dataframes.append(df)

# concat list of dataframes
df = pd.concat(list_of_dataframes)

# Set start and end date****
startdate = datetime(1981, 10, 1, 0)
enddate = datetime(2021, 10, 1, 0)

# Start while loop the runs while dates are within the range selected
while startdate < enddate:
    yr = str(startdate.year)
    mo = startdate.month
    if mo <= 9:
        mo = '0'+ str(startdate.month)
    else:
        mo = str(startdate.month)
    dy = startdate.day
    if dy <= 9:
        dy = '0'+ str(startdate.day)
    else:
        dy = str(startdate.day)

    # Call individual date for gridding
    gdf = gpd.GeoDataFrame(df['d_'+yr+mo+dy], geometry=gpd.points_from_xy(df.Lon, df.Lat))
    gdf.to_file('./tmp/df.shp',crs='EPSG:4326')

    # run gdal Grid function with IDW option and save to tmp folder
    gdal.Grid('./tmp/tmpfile.nc','./tmp/df.shp', algorithm = "invdist", zfield='d_'+yr+mo+dy,
                        outputBounds = [ulx,uly,lrx,lry], width=40,height=40, format='netCDF') # roughly 4km
                        
    # match the res/extent of PRISM nc (4km) and save with datestring as filename
    os.system('ncremap -d ./prism_nc/198110.nc ./tmp/tmpfile.nc ./snotel_grids/'+yr+mo+dy+'.nc')

    # Delete files in tmp folder
    shutil.rmtree('./tmp') 
    os.mkdir('./tmp')

    # Jump back up to top of main loop to do next day
    startdate = startdate + timedelta(days=1)
