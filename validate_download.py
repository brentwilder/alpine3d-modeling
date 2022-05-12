# CHECK FOR DUPLICATES TOO!!!! 
from pathlib import Path
from datetime import datetime,timedelta
import pandas as pd

startdate = datetime(1981, 10, 1, 0)
enddate = datetime(2021, 10, 1, 0)
df = pd.DataFrame(columns=['file'])
files=[]

# loop through time to output all corrected hourly TA
while startdate < enddate:
    # There's probably a better way to do this....
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

    # write file if does not exist
    if not myfile.is_file():
        files.append([myfile])

    # Jump back up to top of main loop to do next hour
    startdate = startdate + timedelta(hours=1)

 # Save it to a dataframe
df = pd.DataFrame(files,columns=['file'])
df.to_csv('./verify.csv')
