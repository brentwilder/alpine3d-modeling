# Script to prep forcings for Alpine3D 
# Brent Wilder
# 04/26/2022

# Things it will do:
# Convert specific humidity to relative humidity
# Calculate WS vector from U10 and V10 wind data
# Bias correct air temp and precip with PRISM
# Output all variables: TA, RH, WS, PSUM, ISWR, ILWR

# NOTE: for PRISM bias correction
# Output TA and PSUM from PRISM correction
# PRISM (match cumulative precip, monthly average temp)
# BW EDIT, PRISM is in C and NLDAS is in K.
# Will need to devise a way to group data monthly... and loop through.
# also keep in mind that PRISM at 4KM and NLDAS is 10KM (match NLDAS)
