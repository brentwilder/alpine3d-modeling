# Compute all forcings for alpine3d 
# Brent Wilder
# 05/04/2022

# Import libraries
from datetime import datetime, timedelta
import xarray as xr
import metpy.calc as mpcalc

# Set start and end date
startdate = datetime(1981, 10, 1, 0)
enddate = datetime(2021, 10, 1, 0)

# Create a smaller bounds to get rid of no data (avoiding possible lapse function issues)
# But still leaving enough area to pick up some of the lower elevations to improve the function
lat_bnds, lon_bnds = [43.1004031922779163  , 44.8985620400704235], [-116.9075152150912800, -114.1032432490848834]

# loop through time to output all corrected hourly TA
while startdate < enddate:

    # times for NLDAS
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

    # Select NLDAS based on timestring
    ds = xr.open_dataset('./nldas_match/NLDAS_'+yr+mo+dy+hr+'00.nc')

    # Load in the prism correction files
    corrTA = xr.open_dataset('./nldas_correction_tair/correction_'+yr+mo+'.nc')
    corrPPT = xr.open_dataset('./nldas_correction_precip/correction_'+yr+mo+'.nc')

    # Apply correction to air temperature across grid
    ds['TAtmp'] = ds['Tair'] + corrTA['Band1']
    ds['TA'] = ds.TAtmp.assign_attrs(units='K')

    # Apply correction to precip across grid
    ds['PSUMtmp'] = ds['Rainf'] + corrPPT['Band1']
    # If corrected precip drops to below zero, set to zero...
    # This can happen for dry periods... this makes sense to set these
    # values to zero as we can not have negative precip!
    ds['PSUMtmp'] = ds['PSUMtmp'].where(ds['PSUMtmp']>0,0)
    # Reassign units
    ds['PSUM'] = ds.PSUMtmp.assign_attrs(units='mm/hr')

    # Calc Wind forcings
    ds['WindSpeed'] = mpcalc.wind_speed(ds['Wind_E'], ds['Wind_N'])
    ds['WindDirection'] = mpcalc.wind_direction(ds['Wind_E'], ds['Wind_N'])

    # Compute RH forcings using the corrected Tair
    ds['RH'] = mpcalc.relative_humidity_from_specific_humidity(ds['PSurf'], ds['TA'], ds['Qair'])

    # Clip to smaller area
    ds = ds.sel(lat=slice(*lat_bnds), lon=slice(*lon_bnds))

    # Output the forcings individually
    # Since this is a lot of data (TBs), this is being saved directly to an external hard drive
    ds['TA'].to_netcdf(path='./computed_forcings/TA/TA_'+yr+mo+dy+hr+'00.nc', mode='w')
    ds['PSUM'].to_netcdf(path='./computed_forcings/PSUM/PSUM_'+yr+mo+dy+hr+'00.nc', mode='w')
    ds['RH'].to_netcdf(path='./computed_forcings/RH/RH_'+yr+mo+dy+hr+'00.nc', mode='w')
    ds['LWdown'].to_netcdf(path='./computed_forcings/ILWR/ILWR_'+yr+mo+dy+hr+'00.nc', mode='w')
    ds['SWdown'].to_netcdf(path='./computed_forcings/ISWR/ISWR_'+yr+mo+dy+hr+'00.nc', mode='w')   
    
    # Finally, remove everything except the wind vector (direction and speed)
    ds = ds.drop(labels=['CAPE','CRainf_frac','LWdown','PotEvap',
                         'PSurf','Qair','SWdown','Wind_E','Wind_N',
                         'Tair','TA','PSUM','RH','Rainf','TAtmp','PSUMtmp'])
    ds.to_netcdf(path='./computed_forcings/VW/VW_'+yr+mo+dy+hr+'00.nc', mode='w')

    # Jump back up to top of main loop to do next hour
    startdate = startdate + timedelta(hours=1)

    # Close datasets
    ds.close()
    corrTA.close()
    corrPPT.close()

    # Info output
    print('[INFO] Wrapping up forcings for ',yr,'-',mo,'-',dy,' ',hr)
