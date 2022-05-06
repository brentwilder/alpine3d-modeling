# alpine3d-modeling

### current forcing data workflow
 1. `get_nldas2.py` to download all the hourly data
 1. `get_prism.ipynb` to download monthly Tair/Precip data
 1. `merge_nldas.py` to combine netcdf files and match extent/res of prism
 1. `compute_corrections.py` to calculate Tair/Precip corrections based on prism
 1. `compute_forcings.py` to calc/correct forcing variables and format for alpine3d
 1. `match_dem_grid.ipynb` expensive task of downscaling the grid to match dem
 1.  Run WindNinja to improve wind forcings https://weather.firelab.org/windninja/
 1.  Begin modeling in alpine3d
