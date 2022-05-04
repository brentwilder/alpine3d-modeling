# Script to prep forcings for Alpine3D 
# Brent Wilder
# 04/26/2022

# From here loading in the prism_corrected_nldas:
#   Then, use MetPy to :
#       Calc VW vector from U10 and V10 wind data (later to be ran through WindNinja)
#       return VW to folder

#   MetPy Calc RH from Air T, Pressure, and SH
#       return RH

# Output all variables: TA, RH, VW, PSUM, ISWR, ILWR
