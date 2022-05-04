# alpine3d-modeling

### current forcing data workflow
 1. `get_nldas2.py` to download all the hourly data
 1. `get_prism.ipynb` to download monthly air temp data
 1. `merge_nldas.py` to combine netcdf files and match extent/res of prism
 1. `compute_forcings.py` to calc/correct forcing variables in format for alpine3d
