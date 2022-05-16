# Merge NLDAS-2 and match extent and scale of PRISM
# Brent Wilder
# 05/15/2022

# Import libraries
import os
import xarray as xr

ds = xr.open_mfdataset('nldas/NLDAS_FORA0125_H.A*.nc',combine='nested', concat_dim="time")
ds.to_netcdf('./nldas_merged/nldas.nc')

# Match scale and extent of first prism dataset in the folder (4km)
# This is done in order to bias correct air temp in the next script
# sudo apt install nco for this function
os.system('ncremap -d ./prism_tair_nc/198110.nc ./nldas_merged/nldas.nc ./nldas_merged_nldas_4km.nc')
