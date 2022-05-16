# Compute monthly Tair/Precip correction 
# Brent Wilder
# 05/06/2022

# Import libraries
from datetime import datetime, timedelta
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
        
        # Get the month string from the filename
        # for some reason xarray resample tool
        # will show the last day of the month as the output instead of first day
        # ... to correct for this i simply use a time delta of one day
        thedate = file[:-3]
        thedate = (datetime.strptime(thedate,'%Y%m').date()) - timedelta(days=1)
        
        # prep dates for prism
        month = thedate.month
        year = thedate.year

        # Prep the dates for nldas...
        yr = str(thedate.year)
        mo = thedate.month
        if mo <= 9:
            mo = '0'+ str(thedate.month)
        else:
            mo = str(thedate.month)

        # Temp merge of this specific month NLDAS for averaging
        tmp_merge = xr.open_mfdataset('./nldas_match/NLDAS_'+yr+mo+'*.nc', combine='nested', concat_dim="time")
        tmp_merge.to_netcdf('./tmp/tmp_merge.nc')
        tmp_merge.close()

        # Load this temp file in
        ds = xr.open_dataset('./tmp/tmp_merge.nc')

        # Calculate the monthly means from NLDAS
        monthly_nldas = ds.resample(time='M').mean()
        monthly_nldas_sum = ds.resample(time='M').sum()

        # Convert date back to a string to select timestamp
        thedate = thedate.strftime('%Y-%m-%d')
        nldas_bias_map = monthly_nldas.sel(time=thedate)

        # Subtract the two grids and save as correction (converting to Kelvin)
        nldas_bias_map['correction_tair'] = (prism['tmean']+273.15) - nldas_bias_map['Tair']

        # Save prism tair data just for reference later
        nldas_bias_map['prism_tair'] = prism['tmean'] + 273.15

        # since the filename is same (and also monthly), can take care of precip correction here
        prism.close()
        prism = xr.open_dataset('./prism_precip_nc/'+filename)

        # Have to load as side dataset because we sum precip instead of avg for tair
        nldas_bias_precip = monthly_nldas_sum.sel(time=thedate)
        
        # Get number of hours in this month for the conversion
        hours = monthrange(year, month)[1] * 24

        # Subtract the two grids and save as correction (hourly by averaging per month) [mm / hr]
        nldas_bias_map['correction_precip'] = (prism['ppt'] - nldas_bias_precip['Rainf']) / hours

        # Save prism precip data just for reference later
        nldas_bias_map['prism_ppt'] = prism['ppt']

        # Drop extra variables
        nldas_bias_map = nldas_bias_map.drop(labels=['CAPE','CRainf_frac','LWdown','PotEvap','PSurf','Qair','SWdown','Wind_E','Wind_N'])

        # Write this correction result to .nc in nldas_correction
        output = file[:-3] + '_correction.nc'
        nldas_bias_map.to_netcdf(path='./nldas_correction_prism/'+output, mode='w')
        
        # Close all datasets
        prism.close()
        nldas_bias_map.close()
        nldas_bias_precip.close()
        monthly_nldas.close()
        monthly_nldas_sum.close()
        ds.close()

        # Reset the tmp directory
        shutil.rmtree('./tmp') 
        os.mkdir('./tmp')
