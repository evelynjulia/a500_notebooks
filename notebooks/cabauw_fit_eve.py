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
#     number_sections: false
#     sideBar: false
#     skip_h1_title: true
#     title_cell: Table of Contents
#     title_sidebar: Contents
#     toc_cell: true
#     toc_position: {}
#     toc_section_display: false
#     toc_window_display: false
# ---

# %% [markdown] {"toc": true}
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#2am-UTC" data-toc-modified-id="2am-UTC-1">2am UTC</a></span></li><li><span><a href="#Q1-2:00-UTC----fill-in-the-the-cell-above-to-plot-the-curve-fit-on-top-of-the-hourly-average" data-toc-modified-id="Q1-2:00-UTC----fill-in-the-the-cell-above-to-plot-the-curve-fit-on-top-of-the-hourly-average-2">Q1 2:00 UTC -- fill in the the cell above to plot the curve fit on top of the hourly average</a></span></li><li><span><a href="#Q2--repeat-this-for-10:00--UTC-above" data-toc-modified-id="Q2--repeat-this-for-10:00--UTC-above-3">Q2  repeat this for 10:00  UTC above</a></span></li><li><span><a href="#Q3:-repeat-this-for-14:00--UTC-above" data-toc-modified-id="Q3:-repeat-this-for-14:00--UTC-above-4">Q3: repeat this for 14:00  UTC above</a></span></li><li><span><a href="#Plot-all-hours-with-fits" data-toc-modified-id="Plot-all-hours-with-fits-5">Plot all hours with fits</a></span></li><li><span><a href="#Buoyancy-flux-and-L" data-toc-modified-id="Buoyancy-flux-and-L-6">Buoyancy flux and L</a></span></li></ul></div>

# %% [markdown]
# # Replace my month with yours and fill in the curve fits for 2am, 10am and 2pm

# %%
import glob
from netCDF4 import Dataset
from dateutil.parser import parse
import datetime
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pytz
from datetime import datetime as dt

# %%
import numpy as np
from scipy.optimize import curve_fit
import scipy
from scipy.stats.distributions import  t
import warnings
warnings.filterwarnings("ignore",category=scipy.optimize.OptimizeWarning)

# %% [markdown]
# # read in the Nov 2018 profiles

# %%
the_file='cabauw_nov_2018.nc'
group='m201811'
with Dataset(the_file,'r') as nc_ubc:
    nov_nc=nc_ubc.groups[group]
    z=nc_ubc.variables['z'][...]
    nov_speed=nov_nc.variables['F'][...]
    nov_ta002 = nov_nc.variables['TA002']

nov_speed.shape

# %% [markdown]
# # calculate hourly averages

# %%
hourly_wind_avg=nov_speed.mean(axis=2)

# Calculate monthly average
month_av = nov_speed.mean(axis=(0,2))

# %%

# %%
the_month='nov, 2018'
hour=2
fig,ax=plt.subplots(1,3,figsize=(10,6))
ax[0].plot(hourly_wind_avg[:,hour,:].T,z)
ax[0].plot(month_av[hour,:],z,'k-',linewidth=4)
ax[0].set(title='hour: {} UTC'.format(hour))

hour=10
ax[1].plot(hourly_wind_avg[:,hour,:].T,z)
ax[1].plot(month_av[hour,:],z,'k-',linewidth=4)
ax[1].set(title='hour: {} UTC'.format(hour))
fig.suptitle('{} hourly avg winds'.format(the_month))

hour=14
ax[2].plot(hourly_wind_avg[:,hour,:].T,z)
ax[2].plot(month_av[hour,:],z,'k-',linewidth=4)
ax[2].set(title='hour: {} UTC'.format(hour))
fig.suptitle('{} hourly avg winds'.format(the_month));


# %% [markdown]
# # Fit the wind profiles to a modified log(z) function 

# %% [markdown]
# Follow [Verkaik and Holtslag, 2007](http://ezproxy.library.ubc.ca/login?url=http://link.springer.com/10.1007/s10546-006-9121-1) and fit the windspeed to a modified log profile using scipy.optimize.curve_fit (see their page 710 below equation 1)
#
# ```
# S=a0 + a1*z + a2*z**2 + a3*np.log(z)
# direc=b0 + b1*z + b2*z**2
# theta=c0 + c1*z + c2*z**2. + c3*np.log(z)
# ```

# %%
# def wind_func(z, *coeffs):
#     'nonlinear function in a and to fit to data'
#     fit = coeffs[0] + coeffs[1]*z + coeffs[2]*z**2. + coeffs[3]*np.log(z)
#     return fit

# %%
def wind_func(z,a0,a1,a2,a3):
    'nonlinear function in a and to fit to data'
    fit = a0 + a1*z + a2*z**2. + a3*np.log(z)
    return fit


# %% [markdown]
# ## 2am UTC

# %%
# %matplotlib inline
# 2 UTC
hour1=2 # early morning
day=19 

fig,ax=plt.subplots(1,3,figsize=(10,6))
sample1=nov_speed[day,hour,:,:]
fig.suptitle('U profiles for day {} at {} UTC'.format(day,hour1))
ax[0].plot(sample1.T,z)
ax[0].set(title='6 10 minute samples',xlabel='wind speed (m/s)',
         ylabel='height (m)')
ax[1].plot(hourly_wind_avg[day,hour1,:],z)
ax[1].set(title='hourly average')
ax[2].plot(hourly_wind_avg[day,hour1,:],z, label='Observation')
ax[2].set(title='hourly average plus interpolated values')
# ax[2].plot(fit2am,z, label = 'Fit')
# ax[2].legend()
#
# flip tower data so it goes from bottom to top
# and get rid of the lowest level, which doesn't
# have a measurement
#
rev_z=z[::-1]
rev_z=rev_z[1:]
test=hourly_wind_avg[day,hour1,::-1]
#
# lose the bottom value
#
test=test[1:]

# curve fitting:
#coeffs2am, covar2am = curve_fit(wind_func, z, hourly_wind_avg[day,hour1,:])

month_test = month_av[hour1,::-1]
month_test=month_test[1:]
coeffs2am, covar2am = curve_fit(wind_func, rev_z, month_test)
#coeffs2am, covar2am = curve_fit(wind_func, z, month_av[hour1,:])

#coeffs2am, covar2am = curve_fit(wind_func, rev_z, test)


# to interpolate between height levels
z_interp = np.arange(1,201,0.5)
fit2am = wind_func(z_interp, *coeffs2am)
#plot
ax[2].plot(fit2am,z_interp, 'r-',label = 'Fit (monthly av)',alpha=0.6);
ax[2].legend();


print(f'fit coefficients for {hour1}am:')
for i in coeffs2am:
    print(f"{i:0.4}")

# %% [markdown]
# ## Q1 2:00 UTC -- fill in the the cell above to plot the curve fit on top of the hourly average

# %%
# 10 UTC
hour2=10 # later morning


fig,ax=plt.subplots(1,3,figsize=(10,6))
fig.suptitle('U profiles for day {} at {} UTC'.format(day,hour2))
sample2=nov_speed[day,hour2,:,:]
ax[0].plot(sample2.T,z)
ax[0].set(title='6 10 minute samples',xlabel='wind speed (m/s)',
         ylabel='height (m)')
ax[1].plot(hourly_wind_avg[day,hour2,:],z)
ax[1].set(title='hourly average')
ax[2].plot(hourly_wind_avg[day,hour2,:],z, label='Observation')
ax[2].set(title='hourly average plus interpolated values')

#
# flip tower data so it goes from bottom to top
# and get rid of the lowest level, which doesn't
# have a measurement
#
rev_z=z[::-1]
rev_z=rev_z[1:]
test2=hourly_wind_avg[day,hour2,::-1]
test2=test2[1:]

# curve fitting:
# coeffs10am, covar10am = curve_fit(wind_func, z, hourly_wind_avg[day,hour2,:])
# fit10am = wind_func(z, *coeffs10am)
# ax[2].plot(fit10am,z, label = 'Fit')
# ax[2].legend()



month_test2 = month_av[hour2,::-1]
month_test2=month_test2[1:]
coeffs10am, covar10am = curve_fit(wind_func, rev_z, month_test2)


#coeffs10am, covar10am = curve_fit(wind_func, rev_z, test2)

# to interpolate between height levels
#z_interp = np.arange(1,201,0.5)
fit10am = wind_func(z_interp, *coeffs10am)
#plot
ax[2].plot(fit10am,z_interp, 'r-',label = 'Fit (monthly av)',alpha=0.6);
ax[2].legend();


print(f'fit coefficients for {hour2}am:')
for i in coeffs10am:
    print(f"{i:0.4}")

# %% [markdown]
# ## Q2  repeat this for 10:00  UTC above

# %%
# 14 UTC
hour3=14 # afternoon

fig,ax=plt.subplots(1,3,figsize=(10,6))
fig.suptitle('U profiles for day {} at {} UTC'.format(day,hour3))
sample3=nov_speed[day,hour3,:,:]
ax[0].plot(sample3.T,z)
ax[0].set(title='6 10 minute samples',xlabel='wind speed (m/s)',
         ylabel='height (m)')
ax[1].plot(hourly_wind_avg[day,hour3,:],z)
ax[1].set(title='hourly average')
ax[2].plot(hourly_wind_avg[day,hour3,:],z, label='Observation')
ax[2].set(title='hourly average plus interpolated values')


#
# flip tower data so it goes from bottom to top
# and get rid of the lowest level, which doesn't
# have a measurement
#
rev_z=z[::-1]
rev_z=rev_z[1:]

test3=hourly_wind_avg[day,hour3,::-1]
test3=test3[1:]

# curve fitting:
# coeffs14pm, covar14pm = curve_fit(wind_func, z, hourly_wind_avg[day,hour3,:])
# fit14pm = wind_func(z, *coeffs14pm)
# ax[2].plot(fit14pm,z, label = 'Fit')
# ax[2].legend()

month_test3 = month_av[hour3,::-1]
month_test3=month_test3[1:]
coeffs14pm, covar14pm = curve_fit(wind_func, rev_z, month_test3)


#coeffs14pm, covar14pm = curve_fit(wind_func, rev_z, test3)

# to interpolate between height levels
#z_interp = np.arange(1,201,0.5)
fit14pm = wind_func(z_interp, *coeffs14pm)
#plot
ax[2].plot(fit14pm,z_interp, 'r-',label = 'Fit (monthly av)',alpha=0.6);
ax[2].legend();


print(f'fit coefficients for {hour3}am:')
for i in coeffs14pm:
    print(f"{i:0.4}")

# %% [markdown] {"trusted": true}
# ## Q3: repeat this for 14:00  UTC above

# %% [markdown]
# ## Plot all hours with fits

# %%
the_month='nov, 2018'
hour=2
fig,ax=plt.subplots(1,3,figsize=(10,6))
ax[0].plot(hourly_wind_avg[:,hour,:].T,z)
ax[0].plot(fit2am,z_interp, 'k-',label = 'Fit (monthly av)',linewidth=4);
ax[0].set(title='hour: {} UTC'.format(hour))
hour=10
ax[1].plot(hourly_wind_avg[:,hour,:].T,z)
ax[1].plot(fit10am,z_interp, 'k-',label = 'Fit (monthly av)',linewidth=4);
ax[1].set(title='hour: {} UTC'.format(hour))
fig.suptitle('{} hourly avg winds'.format(the_month))
hour=14
ax[2].plot(hourly_wind_avg[:,hour,:].T,z)
ax[2].plot(fit14pm,z_interp, 'k-',label = 'Fit (monthly av)',linewidth=4);
ax[2].set(title='hour: {} UTC'.format(hour))
fig.suptitle('{} hourly avg winds'.format(the_month));
plt.legend();


# black line is the average fit

# %% [markdown]
# # calculate L

# %%
with Dataset(the_file,'r') as nc_ubc:
    nov_nc=nc_ubc.groups[group]
    H=nov_nc.variables['H'][...]
    LE = nov_nc.variables['LE'][...]
    USTAR = nov_nc.variables['UST'][...]
    TA002 = nov_nc.variables['TA002'][...]
    Q002 = nov_nc.variables['Q002'][...]
    P0 = nov_nc.variables['P0'][...]
    timevec = nov_nc.variables['time'][...]
    timevec = [dt.fromtimestamp(item,pytz.utc) \
               for item in timevec.flat]
    
Rd=287.  #J/kg/K
# cp = 1004.  #J/kg/K
k = 0.4
g=9.8
rho = P0*1.e2/(Rd*(TA002 + 273.15))



# %% [markdown]
# ## Buoyancy flux and L

# %%
#fleagle and bussinger eq. 6.31
Eb = H + 0.02*LE
#virtural temperature 
Tv = TA002 + 273.15  + 0.61*Q002*1.e-3
#Fleagle and Businger 6.47
L = - Tv*cp*rho*USTAR**3./(k*g*Eb)
good = np.abs(Eb) > 1

# %%
fig,ax=plt.subplots(1,1)
out=plt.hist(L[good].flatten(),bins=np.linspace(-150,150,40))

# %%
fig,ax=plt.subplots(1,1,figsize=(8,6))
fig.autofmt_xdate()
ax.plot(timevec,L.flatten())
title='Obukhov length L {}'.format(the_month)
out=ax.set(title=title,ylabel='L $(m)$',ylim=[-150,150])

# %%
plt.semilogy(fit14pm,z_interp, 'k-',label = 'Fit (monthly av)',linewidth=2);

# %%
z0 = 0.2
# from Businger Dyer notes
u = USTAR*(k**-1) *(np.log(z[1:]/z0)+(5*z[1:]/L))

# %%
plt.plot(u[19,hour3,:],z[1:])

# %%
plt.semilogy(u[19,hour3,:],z[1:])

# %%

# %%
