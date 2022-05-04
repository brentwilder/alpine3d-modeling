# Script needs to do the following,
# loop through all of nldas data to:
#   match nldas scale/extent to prism
#   take average for each day (24 hours)
#   of the daily avgs, take monthly average for those values
#   compare those monthly averages to prism to find bias
#   "add" this bias correction to the nldas netcdf
#   write to new folder

# TODO: also, would be neat to save this air temp bias correction for reference later for write up
