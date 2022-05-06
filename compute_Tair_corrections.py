# Compute monthly Tair correction 
# Brent Wilder
# 05/04/2022

# Import libraries
from datetime import datetime, timedelta
import xarray as xr
import os

# Call in merged+aligned nldas .nc file and create monthly variable
ds = xr.open_dataset('./nldas_merged/nldas_4km.nc')
monthly_nldas = ds.resample(time='M').mean()

# Loop through all of prism .nc files
for file in os.listdir('./prism_nc'):
    filename = os.fsdecode(file)
    if filename.endswith('.nc'):
        
        # Within this loop, read in file
        prism = xr.open_dataset('./prism_nc/'+filename)
        
        # Get the month string from the filename
        # for some reason xarray resample tool
        # will show the last day of the month as the output instead of first day
        # ... to correct for this i simply use a time delta of one day
        thedate = file[:-3]
        thedate = (datetime.strptime(thedate,'%Y%m').date()) - timedelta(days=1)

        # Convert date back to a string to select timestamp
        thedate = thedate.strftime('%Y-%m-%d')
        nldas_bias_map = monthly_nldas.sel(time=thedate)

        # Subtract the two grids and save as correction (converting to Kelvin)
        nldas_bias_map['correction'] = (prism['tmean']+273.15) - nldas_bias_map['Tair']

        # Save prism data just for reference later
        nldas_bias_map['prism'] = prism['tmean'] + 273.15

        # Drop extra variables
        nldas_bias_map = nldas_bias_map.drop(labels=['CAPE','CRainf_frac','LWdown','PotEvap','PSurf','Qair','SWdown','Rainf','Wind_E','Wind_N'])

        # Write this correction result to .nc in nldas_correction
        output = file[:-3] + '_correction.nc'
        nldas_bias_map.to_netcdf(path='./nldas_correction_prism/'+output, mode='w')
        
        # Close all datasets
        prism.close()
        nldas_bias_map.close()

# Close all datasets
monthly_nldas.close()
ds.close()
