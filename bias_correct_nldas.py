# Bias correct NLDAS-2 air temperature using monthly PRISM
# Brent Wilder
# 05/04/2022

# Import libraries
import xarray as xr
import os

# Call in merged+aligned nldas .nc file and create monthly variable
ds = xr.open_dataset('./nldas_merged/nldas_4km.nc')
monthly_nldas = ds.resample(freq = 'm', dim = 'time', how = 'mean')

# Loop through all of prism .nc files
for file in os.listdir('./prism_nc'):
     filename = os.fsdecode(file)
     if filename.endswith('.nc'):
         # within this loop, read in file
         
         # get the specific month from monthly_nldas

         # subtract the two grids (ds = ds1-ds2) and save as bias
         # repeat these for each month

# After loop is complete... 
# find a way to associate each of the monthly bias back to the respective hourly datasets
