# Compute monthly Tair/Precip correction 
# Brent Wilder
# 05/06/2022

# Import libraries
from datetime import datetime
import xarray as xr
from calendar import monthrange

import os
import shutil

# Loop through all of prism .nc files
for file in os.listdir('./prism_tair_nc'):
    filename = os.fsdecode(file)
    if filename.endswith('.nc'):
        
        # Within this loop, read in file
        prism = xr.open_dataset('./prism_tair_nc/'+filename)
        
        # Get the month/year string from the filename
        thedate = file[:-3]
        thedate = datetime.strptime(thedate,'%Y%m').date()
        year = thedate.year
        month = thedate.month
    
        # Prep the dates..
        yr = str(thedate.year)
        mo = thedate.month
        if mo <= 9:
            mo = '0'+ str(thedate.month)
        else:
            mo = str(thedate.month)

        # Temp merge of this specific month NLDAS for averaging/sum
        # "sudo apt install cdo"
        os.system('cdo ensmean ./nldas_match/NLDAS_'+yr+mo+'*.nc ./tmp/mean.nc')
        os.system('cdo enssum ./nldas_match/NLDAS_'+yr+mo+'*.nc ./tmp/sum.nc')
        # Info output
        print('[INFO] Merge complete ',yr,'-',mo)

        # Load the tmp files from cdo
        nldas_bias_map = xr.open_dataset('./tmp/mean.nc')
        nldas_bias_precip = xr.open_dataset('./tmp/sum.nc')

        # Get just the AVG tair and SUM precip as nc files
        nldas_air = nldas_bias_map['Tair']
        nldas_air.to_netcdf(path='./tmp/tair.nc', mode='w')
        nldas_rain = nldas_bias_precip['Rainf']
        nldas_rain.to_netcdf(path='./tmp/rain.nc', mode='w')

        # save tmp files for prism too
        prism_TA = prism['Band1'] + 273.15
        prism_TA.to_netcdf(path='./tmp/prism_tmean.nc', mode='w')
        prism.close()
        prism_TA.close()
        prism = xr.open_dataset('./prism_precip_nc/'+filename)
        prism_ppt = prism['Band1']
        prism_ppt.to_netcdf(path='./tmp/prism_ppt.nc', mode='w')
        prism.close()
        prism_ppt.close()

        # compute the difference for tair
        os.system('cdo sub ./tmp/prism_tmean.nc ./tmp/tair.nc ./nldas_correction_tair/correction_'+yr+mo+'.nc')

        # Get number of hours in this month for the conversion
        hours = monthrange(year, month)[1] * 24

        # compute the difference for precip
        os.system('cdo sub ./tmp/prism_ppt.nc ./tmp/rain.nc ./tmp/precip_tmp.nc')

        # Load in the differenced precip netcdf
        ds_precip = xr.open_dataset('./tmp/precip_tmp.nc')

        # adjust the precip correction factor back to hourly
        delta_ppt = ds_precip / hours

        # save the precip correction file
        delta_ppt.to_netcdf(path='./nldas_correction_precip/correction_'+yr+mo+'.nc', mode='w')

        # Close all datasets
        ds_precip.close()
        delta_ppt.close()
        nldas_bias_map.close()
        nldas_bias_precip.close()

        # Reset the tmp directory
        shutil.rmtree('./tmp') 
        os.mkdir('./tmp')

        # Info output
        print('[INFO] Wrapping up correction file for ',yr,'-',mo)
