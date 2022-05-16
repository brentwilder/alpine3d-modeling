# Input NLDAS-2 and match extent and scale of PRISM
# Brent Wilder
# 05/15/2022

# Import libraries
import os
from datetime import datetime, timedelta

# Set start and end date
startdate = datetime(1981, 10, 1, 0)
enddate = datetime(2021, 10, 1, 0)

# loop through time...
while startdate < enddate:

    # Prep the dates...
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
    hr = startdate.hour
    if hr <= 9:
        hr = '0'+ str(startdate.hour)
    else:
        hr = str(startdate.hour)

    # Match scale and extent of first prism dataset in the folder (4km)
    # This is done in order to bias correct air temp in the next script
    # sudo apt install nco for this function
    os.system('ncremap -d ./prism_tair_nc/198110.nc ./nldas/NLDAS_FORA0125_H.A'+yr+mo+dy+'.'+hr+'00.020.nc ./nldas_match/NLDAS_'+yr+mo+dy+hr+'00.nc')

    # Jump back up to top of main loop to do next hour
    startdate = startdate + timedelta(hours=1)
