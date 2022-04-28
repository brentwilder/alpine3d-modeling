# Script to download NLDAS-2
# Brent Wilder
# 04/26/2022

# Import libraries
import os

import xarray as xr
import wget
from datetime import datetime, timedelta

# Input data location and login information
NLDASDataLoc = 'https://hydro1.gesdisc.eosdis.nasa.gov/data/NLDAS/NLDAS_FORA0125_H.2.0'
NLDASUsername = 'username'
NLDASPassword = 'password'

# Set bounds for study
ulx = -117
uly = 45
lrx = -114
lry = 43

# Set start and end date
startdate = datetime(1980, 10, 1, 0)
enddate = datetime(2020, 10, 1, 0)

# Start while loop the runs while dates are within the range selected
while startdate < enddate:

    # Get information for the wget request on this loop
    # These iff statements exist because I needed to include the leading zeros
    yr = str(startdate.year)

    doy = startdate.timetuple().tm_yday
    if doy <= 9:
        doy = '00' + str(startdate.timetuple().tm_yday)
    elif doy <= 99:
        doy = '0' + str(startdate.timetuple().tm_yday)
    else:
        doy = str(startdate.timetuple().tm_yday)

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

    hr = startdate.hour
    if hr <= 9:
        hr = '0'+ str(startdate.hour)
    else:
        hr = str(startdate.hour)


    # Download file from NLDAS-2
    url = NLDASDataLoc+'/'+yr+'/'+doy+'/NLDAS_FORA0125_H.A'+yr+mo+dy+'.'+hr+'00.020.nc'
    # Write in a second while loop to try several times in case 'failed: Network is unreachable.'
    attempts = 0
    while attempts < 10:
        try:
            os.system('wget --user ' + NLDASUsername + ' --password ' + NLDASPassword + ' ' + url)
            # Subset the download to our model domain and save this smaller file
            temp_array = xr.open_dataset('./NLDAS_FORA0125_H.A'+yr+mo+dy+'.'+hr+'00.020.nc')
            mask_lon = (temp_array.lon >= ulx) & (temp_array.lon <= lrx)
            mask_lat = (temp_array.lat >= lry) & (temp_array.lat <= uly)
            clipped = temp_array.where(mask_lon & mask_lat, drop=True)
            clipped.to_netcdf(path='./nldas/NLDAS_FORA0125_H.A'+yr+mo+dy+'.'+hr+'00.020.nc',mode='w')
            # Delete the big file
            os.remove('./NLDAS_FORA0125_H.A'+yr+mo+dy+'.'+hr+'00.020.nc')
            break
        except:
            attempts +=1

    # Jump back up to top of main loop to do next hour
    startdate = startdate + timedelta(hours=1)
