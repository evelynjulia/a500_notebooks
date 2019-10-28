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
# <h1>Find Obukhov length<span class="tocSkip"></span></h1>

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
import numpy as np
import matplotlib.pyplot as plt

# %%
month_file = 'cabauw_nov_2018.nc'

# %% [markdown]
# # Read in data

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


# %% [markdown]
# # Calculate L

# %% [markdown]
# $$
# \mathrm{L}=\frac{-\overline{\theta_{\mathrm{v}}} \mathrm{u}_{*}^{3}}{\mathrm{k} \mathrm{g}(\overline{\mathrm{w}^{\prime} \theta_{\mathrm{v}}^{\prime}})_{\mathrm{s}}}
# $$

# %%
# obukhov length

L = (- pt*(eve_ustar**3)) / (k*g*eve_H)

# %% [markdown]
# # Plotting

# %%
# #from read_cabauw import make_date

# # with Dataset('cabauw_nov_2018.nc','r') as nc:
# #     test_time = make_date(nc)
# #eve_time.flatten().compressed()
# #datetime.fromtimestamp(eve_time.flatten().compressed()[2])

# with Dataset('cabauw_nov_2018.nc','r') as f:
#     the_time=f['m201811'].variables['time'][...]
#     start_date=f['m201811'].variables['product'].date_start_of_data
#     start_date = parse(start_date)
#     time_vec=[]
#     for the_hour in the_time:
#         time_vec.append(start_date + datetime.timedelta(hours=float(the_hour)))
#     time_vec=np.array(time_vec)
#     time_vec=time_vec.reshape(-1,24,6)

# %%
#
# date plotting tips at http://matplotlib.org/users/recipes.html
#
fig,ax=plt.subplots(1,1,figsize=(8,6))
fig.autofmt_xdate()
ax.plot(eve_time.flatten(),eve_H.flatten());
#title=f'sensible heat flux for {the_month}'
#ax.set(title=title,ylabel='H $(W\,m^{-2})$')
#print('finished plot: ',month_dict.keys())

# %%
fig,ax=plt.subplots(1,1,figsize=(8,6))
fig.autofmt_xdate()
ax.plot(eve_time.flatten(),L.flatten());
#title=f'sensible heat flux for {the_month}'
#ax.set(title=title,ylabel='H $(W\,m^{-2})$')
#print('finished plot: ',month_dict.keys())

# %%

# %%

# %%

# %%

# %%

# %%

# %%

# %%
