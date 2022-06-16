# alpine3d-modeling
#### This code was largely based off of Patrick Broxton's MATLAB code for [SnowPALM](https://github.com/broxtopd/SnowPALM)

### current forcing data workflow :mountain_snow:
 1. [`get_nldas2.py`](get_nldas2.py) to download all the hourly data
 1. [`validate_download.py`](validate_download.py) to check for gaps in aquisition
 1. [`get_nldas2_leftover.py`](get_nldas2_leftover.py) to download all data that were previously missed..Run validate again to ensure no missing records
 1. [`get_prism.ipynb`](get_prism.ipynb) to download monthly Tair/Precip data
 1. [`match_nldas.py`](match_nldas.py) to match extent/res of prism
 1. [`compute_corrections.py`](compute_corrections.py) to calculate Tair/Precip corrections based on prism
 1. [`compute_forcings.py`](compute_forcings.py) to calc/correct forcing variables and format for alpine3d
 1.  Begin alpine3d

### directories used :file_folder:
```
 
 ├── computed_forcings       # final forcings for alpine3d
 │   ├── ILWR                # longwave radiation
 │   ├── ISWR                # shortwave radiation
 │   ├── PSUM                # precip
 │   ├── RH                  # relative humidty
 │   ├── TA                  # air temp
 │   ├── VW                  # wind vector
 ├── dem                     # dem for model domain (0.001 degree) 
 ├── nldas                   # download location for loooong NLDAS aquisition
 ├── nldas_correction_prism  # correction factors found from prism
 ├── nldas_match             # Aligning NLDAS to prism
 ├── prism_precip_nc         # converted using gdal and saved here
 ├── prism_precip_tif        # downloaded from GEE notebook
 ├── prism_tair_nc           # converted using gdal and saved here
 ├── prism_tair_tif          # downloaded from GEE notebook
 ├── snotel                  # SWE/temp/precip data for calibration later on
 └── tmp                     # tmp folder used throughout this code
````

### required libraries :floppy_disk:
pandas, xarray, metpy, gdal, ee, geemap, ncremap, cdo
