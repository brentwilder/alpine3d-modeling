# Compute all forcings for alpine3d 
# Brent Wilder
# 05/04/2022

# Import libraries
from datetime import datetime, timedelta
import xarray as xr
import metpy.calc as mpcalc

import os
import shutil

# Set start and end date
# NOTE: important to use the same dates used previously
# There is another on line 94 where start date needs to be reset if changed
startdate = datetime(1981, 10, 1, 0)
enddate = datetime(2021, 10, 1, 0)

# Create a smaller bounds to get rid of no data (avoiding possible lapse function issues)
# But still leaving enough area to pick up some of the lower elevations to improve the function
lat_bnds, lon_bnds = [43.1004031922779163  , 44.8985620400704235], [-116.9075152150912800, -114.1032432490848834]

# Call in merged+aligned nldas .nc file
ds = xr.open_dataset('./nldas_merged/nldas_4km.nc')

##############
# COMPUTE TA #
##############

# loop through time to output all corrected hourly TA
while startdate < enddate:

    # Select TA based on timestring
    timestring = startdate.strftime('%Y-%m-%d %H:%M:%S')
    varTA = ds.sel(time=timestring)

    # Load in the corresponding monthly correction file
    yr = str(startdate.year)

    # There's probably a better way to do this....
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

    corrTa = xr.open_dataset('./nldas_correction_prism/'+yr+mo+'_correction.nc')

    # Apply correction to air temperature across grid
    varTA['TA'] = varTA['Tair'] + corrTa['correction_tair']

    # Save the netcdfs to a tempfolder
    varTA['TA'].to_netcdf(path='./tmp/TA_'+yr+mo+dy+hr+'00.nc', mode='w')

    # Jump back up to top of main loop to do next hour
    startdate = startdate + timedelta(hours=1)

# Close datasets
varTA.close()
ds.close()
corrTa.close()

# Merge all of the netcdfs into one stacked netcdf
ds = xr.open_mfdataset('./tmp/*.nc',combine = 'by_coords', concat_dim='time')
ds = ds.sel(lat=slice(*lat_bnds), lon=slice(*lon_bnds))
ds.to_netcdf('./computed_forcings/TA/a3d_TA.nc')
ds.close()

# Delete files in tmp folder
shutil.rmtree('./tmp') 
os.mkdir('./tmp')
##############



################
# COMPUTE PSUM #
################

# Call in merged+aligned nldas .nc file
ds = xr.open_dataset('./nldas_merged/nldas_4km.nc')

# loop through time to output all corrected hourly PSUM
startdate = datetime(1981, 10, 1, 0) # Reset startdate
while startdate < enddate:

    # Select TA based on timestring
    timestring = startdate.strftime('%Y-%m-%d %H:%M:%S')
    varPSUM = ds.sel(time=timestring)

    # Load in the corresponding monthly correction file
    yr = str(startdate.year)
    # There's probably a better way to do this....
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

    corrPSUM = xr.open_dataset('./nldas_correction_prism/'+yr+mo+dy+'_correction.nc')

    # Apply correction to precip across grid
    varPSUM['PSUM'] = varPSUM['Rainf'] + corrPSUM['correction_precip']

    # Save the netcdfs to a tempfolder
    varPSUM['PSUM'].to_netcdf(path='./tmp/PSUM_'+yr+mo+dy+hr+'00.nc', mode='w')

    # Jump back up to top of main loop to do next hour
    startdate = startdate + timedelta(hours=1)

# Close datasets
varPSUM.close()
corrPSUM.close()
ds.close()

# Merge all of the netcdfs into one stacked netcdf
ds = xr.open_mfdataset('./tmp/*.nc',combine = 'by_coords', concat_dim='time')
ds = ds.sel(lat=slice(*lat_bnds), lon=slice(*lon_bnds))
ds.to_netcdf('./computed_forcings/PSUM/a3d_PSUM.nc')
ds.close()

# Delete files in tmp folder
shutil.rmtree('./tmp') 
os.mkdir('./tmp')
##############




##############
# COMPUTE VW #
##############

# Then, use MetPy to calc wind vector 
# (To be improved by Wind Ninja later on)
# Call in merged+aligned nldas .nc file
ds = xr.open_dataset('./nldas_merged/nldas_4km.nc')

# MetPy Calc RH from Pressure, Corrected AirT, and SH
vw = mpcalc.wind_speed(ds['Wind_E'], ds['Wind_N'])
vw['Direction'] = mpcalc.wind_direction(ds['Wind_E'], ds['Wind_N'])
vw = vw.sel(lat=slice(*lat_bnds), lon=slice(*lon_bnds))
vw.to_netcdf('./computed_forcings/VW/a3d_VW.nc')

# Close dataset
vw.close()
ds.close()
##############



##############
# COMPUTE RH #
##############

# Call in merged+aligned nldas .nc file
ds = xr.open_dataset('./nldas_merged/nldas_4km.nc')
ta = xr.open_dataset('./computed_forcings/TA/a3d_TA.nc')

# MetPy Calc RH from Pressure, Corrected AirT, and SH
rh = mpcalc.relative_humidity_from_specific_humidity(ds['PSurf'], ta['Tair'], ds['Qair'])
rh = rh.sel(lat=slice(*lat_bnds), lon=slice(*lon_bnds))
rh.to_netcdf('./computed_forcings/RH/a3d_RH.nc')

# Close datasets
rh.close()
ta.close()
ds.close()
##############



#####################
# OUTPUT ISWR, ILWR #
#####################

# Call in merged+aligned nldas .nc file
ds = xr.open_dataset('./nldas_merged/nldas_4km.nc')

iswr = ds['SWdown']
iswr = iswr.sel(lat=slice(*lat_bnds), lon=slice(*lon_bnds))
iswr.to_netcdf('./computed_forcings/ISWR/a3d_ISWR.nc')

ilwr = ds['LWdown']
ilwr = ilwr.sel(lat=slice(*lat_bnds), lon=slice(*lon_bnds))
ilwr.to_netcdf('./computed_forcings/ILWR/a3d_ILWR.nc')

# close all datasets
iswr.close()
ilwr.close()
ds.close()
