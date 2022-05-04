# alpine3d-modeling

### current forcing data workflow
 - `get_nldas2.py` to download all the hourly data
 - `get_prism.ipynb` to download monthly air temp data
 - `merge_nldas.py` to combine netcdf files and match extent/res of prism
 - `compute_forcings.py` to calc/correct forcing variables in format for alpine3d
