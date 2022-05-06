# Compute daily precip correction 
# Brent Wilder
# 05/05/2022

# Import libraries
from datetime import datetime
import xarray as xr
import os

# Call in merged+aligned nldas .nc file and create monthly variable
ds = xr.open_dataset('./nldas_merged/nldas_4km.nc')
daily_nldas = ds.resample(time='D').sum()

# Loop through all of snotel_Grids .nc files
for file in os.listdir('./snotel_grids'):
    filename = os.fsdecode(file)
    if filename.endswith('.nc'):

        # Within this loop, read in file
        snotel = xr.open_dataset('./snotel_grids/'+filename)
        
        # Get the day string from the filename
        thedate = file[:-3]
        thedate = datetime.strptime(thedate,'%Y%m%d').date()

        # Convert date back to a string to select timestamp
        thedate = thedate.strftime('%Y-%m-%d')
        nldas_bias_map = daily_nldas.sel(time=thedate)

        # Subtract the two grids and save as correction (daily)
        nldas_bias_map['correction_day'] = snotel['Band1'] - nldas_bias_map['Rainf']

        # Subtract the two grids and save as correction (hourly by averaging) [mm / hr]
        nldas_bias_map['correction_hour'] = (snotel['Band1'] - nldas_bias_map['Rainf']) / 24

        # Save snotel data just for reference later
        nldas_bias_map['snotel'] = snotel['Band1']

        # Drop extra variables
        nldas_bias_map = nldas_bias_map.drop(labels=['CAPE','CRainf_frac','LWdown','PotEvap','PSurf','Qair','SWdown','Tair','Wind_E','Wind_N'])

        # Write this correction result to .nc in nldas_correction
        output = file[:-3] + '_correction.nc'
        nldas_bias_map.to_netcdf(path='./nldas_correction_snotel/'+output, mode='w')
        
        # Close all datasets
        snotel.close()
        nldas_bias_map.close()

        break

# Close all datasets
daily_nldas.close()
ds.close()
