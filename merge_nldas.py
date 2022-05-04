# Merge all NLDAS-2 downloads and match extent and scale of PRISM
# Brent Wilder
# 05/04/2022

# Import libraries
import xarray
import os

# Merge all of the netcdfs into one stacked netcdf
ds = xarray.open_mfdataset('./nldas/NLDAS_FORA0125_H.*.nc',combine = 'by_coords', concat_dim='time')
ds.to_netcdf('./nldas_merged/nldas.nc')

# Match scale and extent of first prism dataset in the folder (4km)
# This is done in order to bias correct air temp in the next script
# sudo apt install nco for this function
os.system('ncremap -d ./prism_nc/198110.nc ./nldas_merged/nldas.nc ./nldas_merged/nldas_4km.nc')
