# Script to download the rest of NLDAS-2 from list generated from 'validate_download.py'
# NASA network error is timing out after 10 tries and skips some files...
# My solution is to just list all of the files not downloaded, and input them here

# Brent Wilder
# 05/12/2022

# Import libraries
import os

import pandas as pd
import xarray as xr
from datetime import datetime

# Input data location and login information
NLDASDataLoc = 'https://hydro1.gesdisc.eosdis.nasa.gov/data/NLDAS/NLDAS_FORA0125_H.2.0'
NLDASUsername = 'username'
NLDASPassword = 'password'

# Set bounds for study
ulx = -117
uly = 45
lrx = -114
lry = 43

# Load the verify dataframe
# this is really just a list of all the downloads leftover
df = pd.read_csv('./verify.csv')
df = df.reset_index()  # make sure indexes pair with number of rows

# Loop through each of the rows in the dataframe
for index,row in df.iterrows():
    # designate filename from row
    filename = './' + row['file']
    # get the date from this row
    thedate =  (datetime.strptime(filename[26:-9],'%Y%m%d.%H'))

    # Do the routine of prepping the dates for NLDAS.... 
    # should wrap this into a function... have used like 4 times..
    yr = str(thedate.year)
    doy = thedate.timetuple().tm_yday
    if doy <= 9:
        doy = '00' + str(thedate.timetuple().tm_yday)
    elif doy <= 99:
        doy = '0' + str(thedate.timetuple().tm_yday)
    else:
        doy = str(thedate.timetuple().tm_yday)
    mo = thedate.month
    if mo <= 9:
        mo = '0'+ str(thedate.month)
    else:
        mo = str(thedate.month)
    dy = thedate.day
    if dy <= 9:
        dy = '0'+ str(thedate.day)
    else:
        dy = str(thedate.day)
    hr = thedate.hour
    if hr <= 9:
        hr = '0'+ str(thedate.hour)
    else:
        hr = str(thedate.hour)

    # Download file from NLDAS-2
    url = NLDASDataLoc+'/'+yr+'/'+doy+'/NLDAS_FORA0125_H.A'+yr+mo+dy+'.'+hr+'00.020.nc'
    os.system('wget --user ' + NLDASUsername + ' --password ' + NLDASPassword + ' ' + url)

    # Subset the download to our model domain and save this smaller file
    temp_array = xr.open_dataset('./NLDAS_FORA0125_H.A'+yr+mo+dy+'.'+hr+'00.020.nc')
    mask_lon = (temp_array.lon >= ulx) & (temp_array.lon <= lrx)
    mask_lat = (temp_array.lat >= lry) & (temp_array.lat <= uly)
    clipped = temp_array.where(mask_lon & mask_lat, drop=True)
    clipped.to_netcdf(path='./nldas/NLDAS_FORA0125_H.A'+yr+mo+dy+'.'+hr+'00.020.nc',mode='w')
    # Delete the big file
    os.remove('./NLDAS_FORA0125_H.A'+yr+mo+dy+'.'+hr+'00.020.nc')
