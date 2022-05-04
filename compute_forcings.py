# Compute all forcings for alpine3d 
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
        month = thedate.month # extract month for use later on to apply bias..

        # Convert date back to a string to select timestamp
        thedate = thedate.strftime('%Y-%m-%d')
        #thedate = '1981-10-31'
        nldas_bias_map = monthly_nldas['Tair'].sel(time=thedate)

        # Subtract the two grids and save as correction (converting to Kelvin)
        nldas_bias_map['correction'] = (prism['tmean']+273.15) - nldas_bias_map['Tair']

        # Write this correction result to .nc in nldas_correction
        
        
        # Close all datasets
        prism.close()
        nldas_bias_map.close()
        monthly_nldas.close()


# Loop through time index in nldas_4km file
# for each file, make a check to see which month it is in,
# then apply correction to that hour and output to TA folder

#   Then, use MetPy to :
#       Calc VW vector from U10 and V10 wind data (later to be ran through WindNinja)
#       return VW to folder

#   MetPy Calc RH from Air T, Pressure, and SH
#       return RH

# Output all other variables: PSUM, ISWR, ILWR


# close all datasets
ds.close()
