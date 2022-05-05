# Compute all forcings for alpine3d 
# Brent Wilder
# 05/05/2022

# Cleaned snotel data from the following paper:
# https://www.pnnl.gov/data-products 

# Import libraries
import pandas as pd

import os

# for each txt file in snotel...
for file in os.listdir('./snotel'):
    filename = os.fsdecode(file)
    if filename.endswith('.txt'):
        # get the lat, lon from the filename
        print(filename)
        lat = 
        lon = 
        
        #df = pd.read_csv('./snotel/bcqc_43.51000_-115.57000.txt', sep='\s{1,}', names=['Year','Month','Day','Precip','MaxT','MinT','MeanT','SWE'], header=None, engine='python')

#   load in the dataframe
#   simplify date column, drop all but date and Precip
#   Convert precip to mm
#   Flip matrix to have dates as column headers (one long row)
#   assign to be a geopandas based on lat/lon
#   save geopandas to tmp folder

# new loop
#   for all geopandas in tmp folder
#   merge together something like,
#   IDX | Geo | Date-1 | ...| Date-n
#   save this merged geopandas to snotel
# delete tmp folder

# load this geopandas with GDAL
# https://gis.stackexchange.com/questions/396995/using-geopandas-geodataframe-in-gdal-grid-for-spatial-interpolation-viz-idw-nea

# Loop through each column (date) to conduct IDW at 4km to NetCDF
#   save this to the tmp folder
#   match the res/extent of PRISM nc and save to snotel_grids with datestring as filename
