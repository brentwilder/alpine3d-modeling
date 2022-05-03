# Script to prep forcings for Alpine3D 
# Brent Wilder
# 04/26/2022

# Things it will do:
# USE MetPy to :
#   Calc VW vector from U10 and V10 wind data (later to be ran through WindNinja)
#   Calc RH from Air T, Pressure, and SH
# Downscale all of these data to 30 meters to match model domain
# Output all variables: TA, RH, VW, PSUM, ISWR, ILWR
