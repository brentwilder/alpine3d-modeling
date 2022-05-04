# Compute all forcings for alpine3d 
# Brent Wilder
# 05/04/2022

# Import libraries
from datetime import datetime, timedelta
import xarray as xr
import os

# loop through time index in nldas_4km file
# for each file, make a check to see which month it is in,
# then apply correction to that hour and output to TA folder

#   Then, use MetPy to :
#       Calc VW vector from U10 and V10 wind data (later to be ran through WindNinja)
#       return VW to folder

#   MetPy Calc RH from Air T, Pressure, and SH
#       return RH

# Output all other variables: PSUM, ISWR, ILWR


# close all datasets
