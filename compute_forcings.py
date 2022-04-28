# Script to prep forcings for Alpine3D 
# Brent Wilder
# 04/26/2022

# Things it will do:
# Calculate VW vector from U10 and V10 wind data
# Then need to downscale data to 30 meter to match DEM file
# and then finally clip this file to the study domain bounds
# Output all variables: TA, RH, VW, PSUM, ISWR, ILWR
