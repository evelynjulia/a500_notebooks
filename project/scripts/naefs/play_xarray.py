
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
import context
from project.scripts.functions import make_theta
import sys

sys.path.append("/Users/catherinemathews/UBC/a500_notebooks/project/scripts")

# print(f"here is the data folder: {context.pro_dir}")

data_dir = "/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/"
ds = xr.open_dataset(data_dir+'all_naefs.nc')




# get variable arrays
varnames = list(ds.variables.keys())

####### CREATE SMALLER XARRAY FOR ONE VARIABLE§    

temp_vals = ['TMP_200mb', 'TMP_250mb', 'TMP_500mb', 
    'TMP_700mb', 'TMP_850mb', 'TMP_925mb', 'TMP_1000mb']

temp_dict = {}
for key in temp_vals:
    temp_dict[key] = ds.variables[key]
ds_temp = xr.Dataset(temp_dict, ds.coords)

############ CREATE PRESSURE DATASET
pres_vals = ['PRES_200mb', 'PRES_250mb', 'PRES_500mb', 
    'PRES_700mb', 'PRES_850mb', 'PRES_925mb', 'PRES_1000mb']
press = [200, 250, 500, 700, 850, 925, 1000]

pres_dict = {}
for i, key in enumerate(pres_vals):
    pres_dict[key] = press[i]
ds_pres = xr.Dataset(pres_dict, ds.coords)


CT_lat = -33
CT_lon = 18 
# slice for just Cape Town
CT_temp = ds_temp.sel(latitude=CT_lat, longitude=CT_lon)
CT_press = ds_pres.sel(latitude=CT_lat, longitude=CT_lon)

#### import make_thetav function

## Theta v xarray
TV_CT = make_theta()


for i, key in enumerate(CT_temp):
    # print(key)
    # print(press[i])
    # print(CT.variables[key].values)
    #### then we can do a calculation and get it working
    test = CT_temp.variables[key].values *press[i]
    print(test)

### need to edit this to work with my xarray
def make_theta(temp,press):
    """
      temp in K
      press in Pa
      returns theta in K
    """
    p0=1.e5
    Rd=287.  #J/kg/K
    cpd=1004.  #J/kg/K

    theta = []

    for i, key in enumerate(temp):
        theta[i]=CT_temp.variables[key].values*(p0/press[i])**(Rd/cpd)
    
    return theta


p0=1.e5
Rd=287.  #J/kg/K
cpd=1004.  #J/kg/K

theta = []

for i, key in enumerate(CT_temp):
    t = CT_temp.variables[key].values*(p0/press[i])**(Rd/cpd)
    theta.append(t)