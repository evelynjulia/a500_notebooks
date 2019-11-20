# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   toc:
#     base_numbering: 1
#     nav_menu: {}
#     number_sections: true
#     sideBar: true
#     skip_h1_title: false
#     title_cell: Table of Contents
#     title_sidebar: Contents
#     toc_cell: false
#     toc_position: {}
#     toc_section_display: true
#     toc_window_display: false
# ---

# %% [markdown]
# # Visualize NAEFS netCDF file

# %% [markdown]
# Eve Wicksteed
#
# 8 November 2019
#
# Script to plot NAEFS forecsat data for one hour over Vancouver

# %%
import glob
from netCDF4 import Dataset
from dateutil.parser import parse
import datetime as dt
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
#import pytz
from datetime import datetime as dt
from a500.utils import ncdump

import numpy as np
from scipy.optimize import curve_fit
import scipy
#from scipy.stats.distributions import  t
#import warnings
#warnings.filterwarnings(“ignore”,category=scipy.optimize.OptimizeWarning)

#from mpl_toolkits.basemap import Basemap
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature
import matplotlib.pyplot as plt

import os
#os.getcwd()
os.environ['PROJ_LIB'] = r'/Users/ewicksteed/anaconda3/pkgs/proj4-5.2.0-h6de7cb9_1006/share/proj'


import matplotlib
cmap=matplotlib.cm.get_cmap('viridis')

from netCDF4 import num2date, date2num

# %%
#file = 'cmc_gec00.t00z.pgrb2f012_BC.nc'
file = 'ncep_gec00.t00z.pgrb2f000_SA.nc'

# %%
data_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/data/naefs/'
date='2016050900/'
# +
with Dataset(data_dir+file) as input:
    ncdump.ncdump(input)
# -


# %%
with Dataset(data_dir+file,'r') as gec00:
    hgt85 = gec00.variables['HGT_850mb'][...]
    lons = gec00.variables['longitude'][...]
    lats = gec00.variables['latitude'][...]
    tmp85 = gec00.variables['TMP_850mb'][...]
    tmp85_units = gec00.variables['TMP_850mb'].units
    time=gec00.variables['time'][...]
    time_units= gec00.variables['time'].units


# %%
# #hgt85.shape
# tmp85.shape
# #lon.shape

#date_of_run = np.squeeze(num2date(time,units=time_units))
date_of_run = num2date(time,units=time_units)[0]



# %%
date_of_run

# %%

# %%
# plt.imshow(np.squeeze(tmp85))

# %% [markdown]
# ## Cartopy test

# %%
# import matplotlib
# cmap=matplotlib.cm.get_cmap('viridis')

proj = crs.PlateCarree()
#proj = crs.RotatedPole(pole_longitude=-177.5, pole_latitude=37.5)


#plt.figure(figsize=(6, 3))
fig, ax = plt.subplots(1, 1, figsize=(9,5))
ax = plt.axes(projection=proj)
ax.set_global()
ax.coastlines()

ax.contourf(lons, lats, np.squeeze(tmp85)) #, transform=data_crs)

#cs=ax.pcolormesh(lons,lats,np.squeeze(tmp85),cmap=cmap,transform=proj,alpha=0.8);

cs=ax.imshow(np.squeeze(tmp85),origin='upper',cmap=cmap,
         transform=proj,alpha=0.8);

cax,kw = matplotlib.colorbar.make_axes(ax,location='bottom',pad=0.05,shrink=0.7);
out=fig.colorbar(cs,cax=cax,extend='both',**kw);
label=out.set_label('85 kPa temperature (K)',size=10);
ax.set_title(f'NAEFS forecast: 85 kPa temperature for {dt.strftime(date_of_run,"%d-%m-%Y")}');



# %%
proj = crs.PlateCarree()
#proj = crs.RotatedPole(pole_longitude=-177.5, pole_latitude=37.5)


#plt.figure(figsize=(6, 3))
fig, ax = plt.subplots(1, 1, figsize=(9,5))
ax = plt.axes(projection=proj)
ax.set_global()
ax.coastlines()

ax.contourf(lons, lats, np.squeeze(tmp85)) #, transform=data_crs)

cs=ax.pcolormesh(lons,lats,np.squeeze(tmp85),cmap=cmap,transform=proj,alpha=0.8);

#cs=ax.imshow(np.squeeze(tmp85),origin='upper',cmap=cmap,transform=proj,alpha=0.8);

cax,kw = matplotlib.colorbar.make_axes(ax,location='bottom',pad=0.05,shrink=0.7);
out=fig.colorbar(cs,cax=cax,extend='both',**kw);
label=out.set_label('85 kPa temperature (K)',size=10);
ax.set_title(f'NAEFS forecast: 85 kPa temperature for {dt.strftime(date_of_run,"%d-%m-%Y")}');



van_lon,van_lat = [-123.1207,49.2827]
van_x,van_y=proj.transform_point(van_lon,van_lat,proj)
print(van_x, van_y);

ax.plot(van_x,van_y,'ro',markersize=4);





# %% [markdown]
# ## See NAEFS temp profiles for Vancouver

# %%
# get temps at different heights:
timestep = 0

# For a certain lat and lon
# VANCOUVER
# choose_lat = 49
# choose_lon = -123  # If data is in eastings and westings
#choose_lon = 360 - 123 # if data is in only eastings

# CAPE TOWN
# 33.9249° S, 18.4241° E
choose_lat = -33
choose_lon = 18 



with Dataset(data_dir+file,'r') as gec00:
#     hgt85 = gec00.variables['HGT_850mb'][0,...]
    lon = gec00.variables['longitude'][...]
    lat = gec00.variables['latitude'][...]
#     tmp1000 = gec00.variables['TMP_1000mb'][timestep,...]
#     tmp925 = gec00.variables['TMP_925mb'][timestep,...]
#     tmp850 = gec00.variables['TMP_850mb'][timestep,...]
#     tmp700 = gec00.variables['TMP_700mb'][timestep,...]
#     tmp500 = gec00.variables['TMP_500mb'][timestep,...]
#     tmp250 = gec00.variables['TMP_250mb'][timestep,...]
#     tmp200 = gec00.variables['TMP_200mb'][timestep,...]
#     tmp100 = gec00.variables['TMP_100mb'][timestep,...]
#     tmp50 = gec00.variables['TMP_50mb'][timestep,...]
#     tmp_units = gec00.variables['TMP_850mb'].units


# convert from all eastings to eastings and westings:
lon_ew = lon.copy()
lon_ew[lon_ew > 180] = lon_ew[lon_ew > 180]-360

# need to get index where lat = choose_lat and where lon = choose_lon
which_lon = lon_ew # if initially just eastings
#which_lon = lon # or lon if eastings and westings

lat_ind = np.where(lat == choose_lat)
lon_ind = np.where(which_lon == choose_lon)

print(lat_ind, lon_ind)
# %%

# %%

# %%
levs = np.array([1000, 925, 850, 700, 500, 250, 200]) #, 100, 50])
varbls = ['TMP', 'RH', 'HGT', 'UGRD', 'VGRD']

#Other variables:
#HGT_500mb
#UGRD_50mb
#VGRD_50mb

all_data = np.zeros((len(levs),len(varbls)))

with Dataset(data_dir+file,'r') as gec00:
    for ind_v, var in enumerate(varbls):
        for ind_l, lev in enumerate(levs):
            var_an_lev = var+'_'+str(lev)+'mb'
            data = gec00.variables[var_an_lev][timestep,...]
            datanew = data[lat_ind, lon_ind]
            all_data[ind_l,ind_v]= datanew


# %%
# now we have an array with a couple of variables (tmp and RH for each model level)
all_data

# %%
fig, ax = plt.subplots(2, 2, figsize=(10,10));
ax[0,0].plot(all_data[:,0],levs, 'ko-', label = 'Temperature');
ax[0,1].plot(all_data[:,1],levs, 'ko-',label = 'RH');
ax[1,0].plot(all_data[:,2],levs, 'ko-', label='height');
ax[1,1].plot(all_data[:,3],levs, 'bo-', label = 'ugrd');
ax[1,1].plot(all_data[:,4],levs, 'ko-', label = 'vgrd');
ax[0,0].invert_yaxis();
ax[0,0].set_title(f'Temperature on {dt.strftime(date_of_run,"%d-%m-%Y")}')
ax[0,1].invert_yaxis();
ax[0,1].set_title(f'Relative Humidity on {dt.strftime(date_of_run,"%d-%m-%Y")}');
ax[1,0].invert_yaxis();
ax[1,0].set_title(f'Geopotential height on {dt.strftime(date_of_run,"%d-%m-%Y")}');
ax[1,1].invert_yaxis();
ax[1,1].set_title(f'U and V wind components on {dt.strftime(date_of_run,"%d-%m-%Y")}')
plt.legend();

# %%
fig, ax = plt.subplots(1,1, figsize=(9,5));
ax.plot(levs, all_data[:,2], 'ko-', label='height');
ax.set_ylim(0,2000)
ax.set_xlim(700,1100)
ax.set_xlabel('pressure (hPa)')
ax.set_ylabel('height (m)')

# %%
fig, ax = plt.subplots(1,1, figsize=(9,5));
ax.plot(all_data[:,0], levs, 'ko-', label='height');
ax.set_xlim(265,300);
ax.set_ylabel('pressure (hPa)')
ax.set_xlabel('Temp (K)')
ax.invert_yaxis();
ax.set_ylim(1100,750);
ax.set_title(f'Temp profile for location on {dt.strftime(date_of_run,"%d-%m-%Y")}');

# %%

# %%

# %%


# %%
# os.getcwd()

# %%
# import subprocess
# subprocess.run("touch 'test_file'", shell=True)

# %%

# %%
