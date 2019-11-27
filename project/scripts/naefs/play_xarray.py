
# Eve Wicksteed
# November 2019
# Work with xarray dataset

import xarray
from netCDF4 import Dataset
from pathlib import Path
import context
from datetime import datetime
from pytz import utc
import matplotlib
from matplotlib import pyplot as plt
import pprint
import xarray as xr
#matplotlib.use("Agg")
from a500.utils import ncdump
import re

data_dir = "/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/"
ds = xr.open_dataset(data_dir+'all_naefs.nc')

# convert temp to theta v?

# first need to create data Array in xarray of temp vars

# get variable arrays
varnames = list(ds.variables.keys())

####### CREATE SMALLER XARRAY FOR ONE VARIABLE§    
#
#
# create an xarray out of these files
#
temp_vals = 
    ['TMP_200mb', 'TMP_250mb', 'TMP_500mb', 
    'TMP_700mb', 'TMP_850mb', 'TMP_925mb', 'TMP_1000mb']

temp_dict = {}
for key in temp_vals:
    temp_dict[key] = ds.variables[key]
ds_temp = xr.Dataset(temp_dict, ds.coords)