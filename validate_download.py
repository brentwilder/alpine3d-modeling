# Finds missing files and exports a list to csv
# This csv can then be fed to get_nldas2_leftover.py
# to catch any missing files...
# Can also check duplicates if for some reason you downloaded a multiple times
# and finally, outputs list of files for merging
# Brent Wilder
# 05/15/22

# Import libraries
from pathlib import Path
from datetime import datetime,timedelta
import pandas as pd

# Set start and end dates
startdate = datetime(1981, 10, 1, 0)
enddate = datetime(2021, 10, 1, 0)

# Initate empty lists for verification, duplicates, and merging
files=[]
duplicates=[]
merges=[]

# loop through time 
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
    hr = startdate.hour
    if hr <= 9:
        hr = '0'+ str(startdate.hour)
    else:
        hr = str(startdate.hour)

    # test file
    myfile = Path('./nldas/NLDAS_FORA0125_H.A'+yr+mo+dy+'.'+hr+'00.020.nc')

    # write file if does not exist yet..
    if not myfile.is_file():
        files.append([myfile])

    # Check if there is a duplicate
    for i in range(1,5):
        myfile_duplicate = Path('./nldas/NLDAS_FORA0125_H.A'+yr+mo+dy+'.'+hr+'00.020('+str(i)+').nc')
        if myfile_duplicate.is_file():
            duplicates.append([myfile_duplicate])

    # Append merge list
    merges.append(['./'+ str(myfile)])

    # Jump back up to top of main loop to do next hour
    startdate = startdate + timedelta(hours=1)

# Save them to dataframes
df = pd.DataFrame(columns=['file'])
df = pd.DataFrame(files,columns=['file'])
df.to_csv('./verify.csv')

df = pd.DataFrame(columns=['file'])
df = pd.DataFrame(duplicates,columns=['file'])
df.to_csv('./duplicates.csv')

df = pd.DataFrame(columns=['file'])
df = pd.DataFrame(merges,columns=['file'])
df.to_csv('./merge_list.csv')
