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
#   latex_envs:
#     LaTeX_envs_menu_present: true
#     autoclose: false
#     autocomplete: true
#     bibliofile: biblio.bib
#     cite_by: apalike
#     current_citInitial: 1
#     eqLabelWithNumbers: true
#     eqNumInitial: 1
#     hotkeys:
#       equation: meta-9
#     labels_anchors: false
#     latex_user_defs: false
#     report_style_numbering: false
#     user_envs_cfg: false
#   toc:
#     base_numbering: 1
#     nav_menu: {}
#     number_sections: true
#     sideBar: false
#     skip_h1_title: false
#     title_cell: Table of Contents
#     title_sidebar: Contents
#     toc_cell: true
#     toc_position: {}
#     toc_section_display: block
#     toc_window_display: false
# ---

# %% [markdown] {"toc": true}
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Read-cabauw-data" data-toc-modified-id="Read-cabauw-data-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Read cabauw data</a></span></li><li><span><a href="#Sorting-by-month" data-toc-modified-id="Sorting-by-month-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Sorting by month</a></span></li><li><span><a href="#Data-first-look" data-toc-modified-id="Data-first-look-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Data first look</a></span></li><li><span><a href="#Checkpoint-all-the-data-into-one-netcdf-file" data-toc-modified-id="Checkpoint-all-the-data-into-one-netcdf-file-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Checkpoint all the data into one netcdf file</a></span></li><li><span><a href="#Eve's-work" data-toc-modified-id="Eve's-work-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Eve's work</a></span><ul class="toc-item"><li><span><a href="#read-in-data" data-toc-modified-id="read-in-data-5.1"><span class="toc-item-num">5.1&nbsp;&nbsp;</span>read in data</a></span></li><li><span><a href="#Calculate-Obukhov-length:-L" data-toc-modified-id="Calculate-Obukhov-length:-L-5.2"><span class="toc-item-num">5.2&nbsp;&nbsp;</span>Calculate Obukhov length: L</a></span></li><li><span><a href="#Plotting" data-toc-modified-id="Plotting-5.3"><span class="toc-item-num">5.3&nbsp;&nbsp;</span>Plotting</a></span></li></ul></li></ul></div>

# %% [markdown] {"collapsed": true}
# To do the sunrise/sunset calculations you'll need to do:
#
# ```
# conda install python-dateutil
# conda install ephem
# ```
#

# %% [markdown] {"trusted": false}
# ####turn this cell from markdown to python to run this import
# ##this is how you install things from inside of jupyter
# import sys
# !conda install --yes --prefix {sys.prefix} ephem python-dateutil

# %% [markdown]
# # Read cabauw data
#
# Data from the [CESAR field campaign](http://ezproxy.library.ubc.ca/login?url=http://link.springer.com/10.1007/s10546-006-9121-1), available from [this web site](<http://www.cesar-database.nl/ShowMyCds.x)
#
# The objective is to download two months of data (july and december 2014) and consolidate it into
# a single netcdf file for later analysis

# %%
import glob
from netCDF4 import Dataset
from dateutil.parser import parse
import context
import datetime
import numpy as np
import matplotlib.dates as mdates
from a500.utils.data_read import download
from a500.utils import ncdump
import a500

filelist=['cesar_surface_flux_lc1_t10_v1.0_201811.nc',
          'cesar_surface_meteo_lc1_t10_v1.0_201811.nc', 
          'cesar_tower_meteo_lc1_t10_v1.0_201811.nc']

# %%
a500.data_dir


# %%
# all_files=a500.data_dir.glob('cesar*lc1_t10_v1.0_201811.nc')
# for the_file in all_files:
#     print(the_file)

# %% [markdown]
# The make_date function takes an open CESAR ncfile and turns the time
# vector from hours past the start date into a python datetime object
# in UTC.  It uses the dateutil parse function to turn the date_start_of_data string into a date.  
#
# This function is used in the cells below to create two dictionaries:
#
# 1. **data_dict** with six keys for the 3 file/2 month combinations
#    with each (file,month) entry holding a dictionary
#    with the numpy array data for the file variables (F, UST, etc.)
#     
# 2. **var_attr** with a key for each variable holding dictionaries with
#    the variable attributes (units, long name, etc.)

# %%
def make_date(ncfile):
    """
    convert cabauw timestamps into python datetime objects

    Parameters
    ----------
    
    ncfile:  Dataset
    
    Returns
    -------
    
    time_vec: ndarray
       numpy array of datetime objects
    """
    the_time=f.variables['time'][...]
    start_date=f.variables['product'].date_start_of_data
    start_date = parse(start_date)
    time_vec=[]
    for the_hour in the_time:
        time_vec.append(start_date + datetime.timedelta(hours=float(the_hour)))
    time_vec=np.array(time_vec)
    time_vec=time_vec.reshape(-1,24,6)
    return time_vec



# %% [markdown]
# Loop through all the files and make a dictionary with keys determined
# by the netcdf file attributes.  Initially the dictionary contains the
# filename, start_date, lat, lon and start time.

# %%
def get_attrs(ncvar):
    """
        get every attribute of a netcdf variable
        
    Parameters
    ----------
    
    ncvar: netcdf variable object

    Returns
    -------
    
    attr_dict: dict
      dictionary with attribute names and values
    """
    attributes=ncvar.ncattrs()
    attr_dict={}
    for attr in attributes:
        attr_dict[attr]=getattr(ncvar,attr)
    return attr_dict
    
all_files=a500.data_dir.glob('cesar*lc1_t10_v1.0_201811.nc')
data_dict={}
var_attrs={}
for the_file in all_files:
    if str(the_file).find('nubiscope') > -1:
        continue
    with Dataset(the_file,'r') as f:
        details=f.variables['iso_dataset']
        attr_dict=get_attrs(details)
        lon=attr_dict['westbound_longitude']
        lat=attr_dict['northbound_latitude']
        title=attr_dict['title'].split()
        the_time = make_date(f)
        #
        # turn a title like:
        #"CESAR surface fluxes validated and gap filled"
        # into the string: surface_fluxes
        #
        filetype='{}_{}'.format(*title[1:3])
        start_date=f.variables['product'].date_start_of_data
        start_date=parse(start_date)
        start_month=start_date.strftime('%Y%m')
    data_dict[filetype,start_month]=dict(name=the_file,timevec=the_time,lon=lon,lat=lat,
                                        start_date=start_date)
#
#  lat and lon shouldn't change, use the last values for the netcdf file attribute
#
for name in ['lat','lon']:
    var_attrs[name]=data_dict[filetype,start_month][name]

# %%
var_attrs

# %% [markdown]
# Now loop through the dictionary and add the flux and tower variables.
# Each variable is a linear vector of measurements taken every 10 minutes, and
# for tower variables, at 7 levels.
#
# The numpy command:
# var.reshape(-1,24,6,7)
# takes the linear vector and folds it into either 28,29,30,31 days (depending on month)
# 24 hours, 6 10 minute intervals, and 7 levels
#
# That allows us to do an hourly average by saying:
# var.mean(axis=2)  to average over the 6 10 minute measurements.

# %% [markdown]
# # Sorting by month
#
# This cell goes through the data_dict dictionaries and combines the six
# (file,month) keys into two dictionaries, one for each month.

# %%
#
# collect all the data from the three files into a dictionary indexed
# by month called month_dict
#
#  use defaultdict(dict) so that every time we add a new month
#  we create an empty dictionary to hold the variables
#  
#
from collections import defaultdict
month_dict=defaultdict(dict)
for the_key in data_dict.keys():
    var_dict=data_dict[the_key]
    the_month=the_key[1]
    print('working on: ',the_month)
    if the_key[0] == 'tower_meteorological':
        with Dataset(var_dict['name'],'r') as f:
            if 'has_time' not in month_dict[the_month]:
                month_dict[the_month]['timevec'] = var_dict['timevec']
                month_dict[the_month]['has_time']=True
            month_dict[the_month]['z'] = f.variables['z'][...]
            for var in ['F','TA','TD','Q','D']:
                month_dict[the_month][var] = f.variables[var][...].reshape(-1,24,6,7)
                var_attrs[var]=get_attrs(f.variables[var])
    elif the_key[0] == 'surface_fluxes': 
        with Dataset(var_dict['name'],'r') as f:
            for var in ['H','UST','LE']:
                month_dict[the_month][var] = f.variables[var][...].reshape(-1,24,6)
                var_attrs[var]=get_attrs(f.variables[var])
    elif the_key[0] == 'meteorological_surface': 
        with Dataset(var_dict['name'],'r') as f:
            for var in ['P0','TA002','Q002','F010']:
                month_dict[the_month][var] = f.variables[var][...].reshape(-1,24,6)
                var_attrs[var]=get_attrs(f.variables[var])
    elif the_key[0] == 'scanning_radiometer':
        pass
    else:
        raise ValueError("didn't recognize {}".format(the_key[0]))
print('finished: ',month_dict.keys())

# %% [markdown]
# We'll need to know sunrise, sunset and solar noon to interpret our
# data.  Here is how you find these with the 
# [pyephem](http://stackoverflow.com/questions/2637293/calculating-dawn-and-sunset-times-using-pyephem) module

# %%
import ephem
for the_month in month_dict.keys():
    var='tower_meteorological'
    start_time=month_dict[the_month]['timevec'][0,0,0]
    cabauw=ephem.Observer()
    cabauw.date=start_time
    cabauw.lon = var_attrs['lon']
    cabauw.lat = var_attrs['lat']
    sunrise=cabauw.next_rising(ephem.Sun())
    noon = cabauw.next_transit(ephem.Sun(),start=sunrise)
    sunset = cabauw.next_setting(ephem.Sun())
    print('sunrise is {} UTC'.format(sunrise))
    print('solar noon {} UTC'.format(noon))
    print('sunset is {} UTC'.format(sunset))

# %% [markdown]
# # Data first look

# %%
from matplotlib import pyplot as plt
plt.show()
plt.style.use('ggplot')
print('starting: ',month_dict.keys())    
for the_month in month_dict.keys():
    hourly_wind_avg = month_dict[the_month]['F'].mean(axis=2)
    z=month_dict[the_month]['z']
    hour=2
    fig,ax=plt.subplots(1,2,figsize=(8,6))
    ax[0].plot(hourly_wind_avg[:,hour,:].T,z)
    ax[0].set(title='hour: {} UTC'.format(hour))
    hour=14
    ax[1].plot(hourly_wind_avg[:,hour,:].T,z)
    ax[1].set(title='hour: {} UTC'.format(hour))
    fig.suptitle('{} hourly avg winds'.format(the_month))

# %%
#
# date plotting tips at http://matplotlib.org/users/recipes.html
#
the_time = month_dict[the_month]['timevec']
H=month_dict[the_month]['H']
print(H.shape)
fig,ax=plt.subplots(1,1,figsize=(8,6))
fig.autofmt_xdate()
ax.plot(the_time.flatten(),H.flatten())
title=f'sensible heat flux for {the_month}'
ax.set(title=title,ylabel='H $(W\,m^{-2})$')
print('finished plot: ',month_dict.keys())


# %% [markdown]
# # Checkpoint all the data into one netcdf file
#
# I want to save month_dict into a netcdf file so we don't need
# to repeat this processing but can start with a merged dataset
# that has all days of interest and all
# instruments in a single place.   To do that, I group the measurements
# into individual days using [netcdf groups](http://unidata.github.io/netcdf4-python)
#
# I transfer all the attributes I read into the var_attrs dict so I maintain
# the original metadata as much as possible

# %%
def write_attrs(ncvar,attr_dict):
    for name,item in attr_dict.items():
        if name != '_FillValue':
            setattr(ncvar,name,item)
    return None

from netCDF4 import Dataset
import os
filename='cabauw_nov_2018.nc'
if os.path.exists(filename):
    os.remove(filename)   
with Dataset(filename,'w') as ncout:
    the_months = month_dict.keys()
    for the_month in the_months:
        speed=month_dict[the_month]['F']
        days_name='days{:2d}'.format(speed.shape[0])
        dimnames=[days_name,'hours','min10','z']
        dim_info=zip(dimnames,speed.shape)
        #
        # this fails gracefully if dimension exists
        #
        for name,length in dim_info:     
            try:
                ncout.createDimension(name,length) 
            except RuntimeError:
                pass
        nc_month='m{}'.format(the_month)
        date_group=ncout.createGroup(nc_month)
        setattr(date_group,'month',the_month)
        for var in ['H','LE','UST','P0','TA002','Q002','F010']:
            the_data=month_dict[the_month][var]
            var_nc=date_group.createVariable(var,the_data.dtype,
                                             [days_name,'hours','min10'])
            var_nc[...]=the_data[...]
            write_attrs(var_nc,var_attrs[var])
        for var in ['TA','D','Q','TD','F']:
            the_data=month_dict[the_month][var]
            var_nc=date_group.createVariable(var,the_data.dtype,
                                             [days_name,'hours','min10','z'])
            var_nc[...]=the_data[...]
            write_attrs(var_nc,var_attrs[var])

        the_time=month_dict[the_month]['timevec']
        float_time=np.array([item.timestamp() for item in the_time.flat])
        float_time=float_time.reshape(-1,24,6)   
        time_nc=date_group.createVariable('time',float_time.dtype,
                                     [days_name,'hours','min10']) 
        time_nc[...]=float_time[...]
        time_nc.timezone='UTC'
        time_nc.comment='convert using datetime.fromtimestamp(var,pytz.utc)'
        try:
            z=month_dict[the_month]['z']
            z_nc=ncout.createVariable('z',z.dtype,['z'])
            z_nc[...]=z[...]
        except RuntimeError:
            #
            # only create ncout z vector once
            #
            pass
        ncout.history='written by read_cabauw.ipynb'
        for var in ['lat','lon']:
            setattr(ncout,var,float(var_attrs[var]))
        ncout.lat_units='degrees north'
        ncout.lon_units='degrees east'
        filelist=[]
        for key,value in data_dict.items():
            filelist.append('{};'.format(value['name']))
        filelista=np.array(filelist)
        setattr(ncout,'filelist',filelist)


# %%
# with Dataset('cabauw_nov_2018.nc') as input:
#     ncdump.ncdump(input)

# %%

# %%
# with Dataset(a500.data_dir /'cesar_surface_flux_lc1_t10_v1.0_201811.nc') as input:
#     ncdump.ncdump(input)
# with Dataset(a500.data_dir /'cesar_surface_meteo_lc1_t10_v1.0_201811.nc') as input:
#     ncdump.ncdump(input)
# with Dataset(a500.data_dir /'cesar_tower_meteo_lc1_t10_v1.0_201811.nc') as input:
#     ncdump.ncdump(input)

# %% [markdown] {"scrolled": true, "trusted": true}
# # Eve's work

# %% {"scrolled": true}
month_file = 'cabauw_nov_2018.nc'

# %% [markdown] {"trusted": true}
# ## read in data

# %%
from netCDF4 import Dataset
with Dataset('cabauw_nov_2018.nc','r') as nc:
    the_groups=nc.groups
    my_groups=list(the_groups.keys())
    eve_H = nc['m201811'].variables['H'][...] # w'thetav'
    eve_press = nc['m201811'].variables['P0'][...]
    eve_temp = nc['m201811'].variables['TA'][...] 
    eve_ustar = nc['m201811'].variables['UST'][...]
    eve_av_temp = nc['m201811'].variables['TA'][...].mean(axis=3) # average temp over height
    eve_time = nc['m201811'].variables['time'][...]


# %%
# constants 

k = 0.4
g = 9.81
p0=1.e5
Rd=287.  #J/kg/K
cpd=1004.  #J/kg/K
pt = eve_av_temp*(p0/eve_press)**(Rd/cpd)#  potential temp --> assume same as vpt


# %% [markdown] {"trusted": true}
# ## Calculate Obukhov length: L

# %% [markdown] {"trusted": true}
# $$
# \mathrm{L}=\frac{-\overline{\theta_{\mathrm{v}}} \mathrm{u}_{*}^{3}}{\mathrm{k} \mathrm{g}(\overline{\mathrm{w}^{\prime} \theta_{\mathrm{v}}^{\prime}})_{\mathrm{s}}}
# $$

# %%
# obukhov length

L = (- pt*(eve_ustar**3)) / (k*g*eve_H)

# %% [markdown] {"trusted": true}
# ## Plotting

# %%
#
# date plotting tips at http://matplotlib.org/users/recipes.html
#
fig,ax=plt.subplots(2,1,figsize=(8,12))
fig.autofmt_xdate();
ax[1].plot(the_time.flatten(),L.flatten());
ax[1].set(title=f'Obukhov length for {the_month}',ylabel='L');
ax[0].plot(the_time.flatten(),eve_H.flatten());
ax[0].set(title=f'Sensible heat flux for {the_month}',ylabel='H $(W\,m^{-2})$');


# %%

# %%

# %%
