# %% [markdown]
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Introduction" data-toc-modified-id="Introduction-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Introduction</a></span><ul class="toc-item"><li><span><a href="#The-Dry-LES-dataset" data-toc-modified-id="The-Dry-LES-dataset-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>The Dry LES dataset</a></span><ul class="toc-item"><li><span><a href="#Intro-to-netcdf" data-toc-modified-id="Intro-to-netcdf-1.1.1"><span class="toc-item-num">1.1.1&nbsp;&nbsp;</span>Intro to netcdf</a></span></li></ul></li><li><span><a href="#Intro-to-python-packages" data-toc-modified-id="Intro-to-python-packages-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Intro to python packages</a></span></li><li><span><a href="#Setting-up-the-environment" data-toc-modified-id="Setting-up-the-environment-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Setting up the environment</a></span></li><li><span><a href="#Intro-to-jupytext" data-toc-modified-id="Intro-to-jupytext-1.4"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>Intro to jupytext</a></span></li><li><span><a href="#Now-download-the-data" data-toc-modified-id="Now-download-the-data-1.5"><span class="toc-item-num">1.5&nbsp;&nbsp;</span>Now download the data</a></span></li><li><span><a href="#Dumping-the-netcdf-metadata" data-toc-modified-id="Dumping-the-netcdf-metadata-1.6"><span class="toc-item-num">1.6&nbsp;&nbsp;</span>Dumping the netcdf metadata</a></span></li><li><span><a href="#Plot-$\theta$-profile-for-every-third-timestep-(i.e.-every-30-minutes)" data-toc-modified-id="Plot-$\theta$-profile-for-every-third-timestep-(i.e.-every-30-minutes)-1.7"><span class="toc-item-num">1.7&nbsp;&nbsp;</span>Plot $\theta$ profile for every third timestep (i.e. every 30 minutes)</a></span></li><li><span><a href="#Color-contour-plot-of-one-level-for-realization-c1,-last-timestep" data-toc-modified-id="Color-contour-plot-of-one-level-for-realization-c1,-last-timestep-1.8"><span class="toc-item-num">1.8&nbsp;&nbsp;</span>Color contour plot of one level for realization c1, last timestep</a></span></li></ul></li><li><span><a href="#Assignment" data-toc-modified-id="Assignment-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Assignment</a></span><ul class="toc-item"><li><span><a href="#a)-Make-a-pcolormesh-plot-for-the-ensemble-averaged-vertical-temperature-flux-at-the-400-meters" data-toc-modified-id="a)-Make-a-pcolormesh-plot-for-the-ensemble-averaged-vertical-temperature-flux-at-the-400-meters-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>a) Make a pcolormesh plot for the ensemble-averaged vertical temperature flux at the 400 meters</a></span></li><li><span><a href="#b)-Plot-horizontally-averaged-vertical-temperature-flux-vs.-height-for-each-of-the-10-ensemble-members" data-toc-modified-id="b)-Plot-horizontally-averaged-vertical-temperature-flux-vs.-height-for-each-of-the-10-ensemble-members-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>b) Plot horizontally averaged vertical temperature-flux vs. height for each of the 10 ensemble members</a></span></li><li><span><a href="#Notes-from-class,-17-September" data-toc-modified-id="Notes-from-class,-17-September-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>Notes from class, 17 September</a></span></li></ul></li></ul></div>

# %%
import sys
import a500
from matplotlib import pyplot as plt
from netCDF4 import Dataset
import numpy as np


# %%
import this

# %% [markdown]
# # Introduction

# %% [markdown]
# ## The Dry LES dataset
#
# This notebook looks at a portion of a dataset that was generated by running a large eddy simulation 10 different times with identical conditions.  The 10 realizations of temperature and pressure are stored as a single netcdf file
#
# ### Intro to netcdf
#
# See the function descriptions and tutorial at http://unidata.github.io/netcdf4-python/
#
# ## Intro to python packages
#
# Start with this general intro:  https://www.learnpython.org/en/Modules_and_Packages
#
# This notebook is part of this git repo: https://github.com/phaustin/a500_notebooks
#
# Clone this repo:
#
# ```
# git clone https://github.com/phaustin/a500_notebooks
# ```
#
# The `a500_notebooks` folder contains a python setup.py file:  https://github.com/phaustin/a500_notebooks/blob/master/setup.py
# which can be used to install a series of helper routines:  
#
# https://github.com/phaustin/a500_notebooks/tree/master/a500/utils
#
# a. To install these using pip, first sync with my repo.
#    
#      cd a500_notebooks
#      git fetch origin
#      git reset --hard origin/master
#  
#  b. Next to an ["editable install"](https://stackoverflow.com/questions/42609943/what-is-the-use-case-for-pip-install-e), so that you can continue to change the module after installation:
#     
#     pip install -e .
#     
#    (this is called an editable install for reasons I'll explain in class)
#    
#    [1]: https://en.wikipedia.org/wiki/Pip_(package_manager)
#  
# b. Check the install by executing the cell below to download a data file.
#
#    If it succeeds, you should see:
#    
#        download case_60_10.nc: size is    499.3 Mbytes

# %% [markdown]
# ## Setting up the environment
#
# You should be able to create an environment called "a500test" by changing into the conda folder and doing:
#
# ```
# conda env create -f environment.yml
# conda activate a500test
# ```
#
# as explained in class
#

# %% [markdown]
# ## Intro to jupytext

# %% [markdown]
# Note that the two notebooks in https://github.com/phaustin/a500_notebooks/tree/master/notebooks both have
# python versions in https://github.com/phaustin/a500_notebooks/tree/master/notebooks/python
#
# In class I'll explain how I use https://github.com/mwouts/jupytext  to pair every ipynb file with a py file that is easier to examine and maintain on github, and how jupyter notebooks can sync the pair of ipynb and py files using
# [jupyter_notebook_config.py](https://github.com/phaustin/a500_notebooks/blob/master/conda/jupyter_notebook_config.py)
#

# %% [markdown]
# ## Now download the data

# %%
from  a500.utils.data_read import download
the_root="http://clouds.eos.ubc.ca/~phil/docs/atsc500/data/"
the_file='case_60_10.nc'
out=download(the_file,root=the_root,dest_folder=a500.data_dir)

# %% [markdown]
# ## Dumping the netcdf metadata
#
# Netcdf file layout:  10 groups corresponding to 10 different ensemble members.  Small slice of larger domain of LES run with surface heat flux of 60 W/m^2 and stable layer with dT/dz = 10 K/km.  Snapshots every 10 minutes for 8 hours.
#
# We can read the metdata using the following utils function:

# %%
from a500.utils.ncdump import ncdump


with Dataset(the_file) as nc_in:
    ncdump(nc_in)


# %% [markdown]
# ## Plot $\theta$ profile for every third timestep (i.e. every 30 minutes)

# %%
def make_theta(temp,press):
    """
      temp in K
      press in Pa
      returns theta in K
    """
    p0=1.e5
    Rd=287.  #J/kg/K
    cpd=1004.  #J/kg/K
    theta=temp*(p0/press)**(Rd/cpd)
    return theta

case_name='case_60_10.nc'
#
#  look at the first ensemble member
#
ensemble='c1'
with Dataset(case_name,'r') as ncin:
    #
    # grab the group variables
    #
    group = ncin.groups[ensemble]
    temp=group.variables['TABS'][...]
    press=ncin.variables['press'][...]
    z=ncin.variables['z'][...]
mean_temp=temp.mean(axis=(3,2))


fig,ax=plt.subplots(1,1,figsize=(10,8))
for i in np.arange(0,temp.shape[0],3):
    theta = make_theta(mean_temp[i,:],press)
    ax.plot(theta,z)
out=ax.set(xlabel=r'$\overline{\theta}$ (K)',ylabel='height (m)',
       title=f'LES dry run for realization {ensemble}:  surface flux=60 $W\,m^{-2}$, $\Gamma$=10 K/km')
ax.grid(True, which='both')


# %%

np.savetxt("dry_les_mean_temp.csv",mean_temp)
np.savetxt("dry_les_press.csv",press)

# %%
temp.shape

# %% [markdown]
# ## Color contour plot of one level for realization c1, last timestep
#
# 1. Find the index of the level closest to 400 meters using searchsorted
# 2. Retrieve the horizontal temperature field for this realization at the last timestep

# %%
index=np.searchsorted(z,400.)
temp_400=temp[-1,index,:,:]


# %%
temp_diff.shape

# %%
temp_diff=temp_400 - temp_400.mean(axis=(0,1))
fig,ax=plt.subplots(1,1,figsize=(10,8))
with Dataset(case_name,'r') as ncin:
    x=ncin.variables['x'][...]
    y=ncin.variables['y'][...]
cs=ax.pcolormesh(x,y,temp_diff)
cb=fig.colorbar(cs)
cb.set_label('temperature perturbation (K)',rotation=-90)


# %% [markdown]
# # Assignment

# %% [markdown]
# This routine from [tropical_boundary_layer.py](https://github.com/phaustin/a500_notebooks/blob/ddeaec7f1baaf6cd25a15ab3c2c436a677136c07/notebooks/python/tropical_boundary_layer.py#L74-L83) calculates the 2-d horizontal spatial mean and the perturbation for a 3-d field like temperature.
#
# ```
# def do_reynolds(array3d):
#     """
#         do a spatial-mean reynolds average of a 3d field array3d
#         needs dimensions arranged as (z,y,x)
#         returns avg(z),perturb(z,y,x)
#     """
#     avg=array3d.mean(axis=2).mean(axis=1)
#     perturb=array3d.T - avg
#     perturb=perturb.T
#     return avg,perturb
# ```

# %% [markdown]
# In the cell below, write a new version that calculates the ensemble mean and the 3-d perturbation for a 3D field like TABS in the dry-les dataset.

# %% [markdown]
# a.) Using your version of do_reynolds, make a pcolormesh plot for the ensemble-averaged vertical temperature flux
# at the 400 meter level for this ensemble

# %% [markdown]
# b.) Plot the horizontally averaged vertical temperature-flux vs. height for each of the 10 ensemble members as 10 lines, to show the variablity in the between individual ensemble members.
#

# %% [markdown]
# ## a) Make a pcolormesh plot for the ensemble-averaged vertical temperature flux at the 400 meters

# %%
def do_reynolds(array3d):
    """
        do a spatial-mean reynolds average of a 3d field array3d
        needs dimensions arranged as (z,y,x)
        returns avg(z),perturb(z,y,x)
    """
    avg=array3d.mean(axis=2).mean(axis=1)
    perturb=array3d.T - avg
    perturb=perturb.T
    return avg,perturb

ensemble=['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10']
with Dataset(case_name,'r') as ncin:
    #
    # grab the group variables
    # and calculate ens average
    #
    temp_tot = 0
    w_tot = 0
    for c in ensemble:
        group = ncin.groups[c]
        temp=group.variables['TABS'][...]
        temp_tot = temp_tot+ temp
        press=ncin.variables['press'][...]
        z=ncin.variables['z'][...]
        w =group.variables['W'][...]
        w_tot= w_tot+w

temp_t1=temp_tot[-1,:,:,:] # temperature for timestep 1
mean_temp=temp_t1/len(ensemble)  ## this is the ensemble mean
w_ens_mean = (w_tot[-1,:,:,:])/len(ensemble)

# get perturbed and 
t_ens_av, t_perturb = do_reynolds(mean_temp) 
w_ens_av, w_perturb = do_reynolds(w_ens_mean)





# %%
# print(mean_temp.shape)
# print(temp_tot.T.shape)
# print(mean_temp[0,...].shape)
# print(ens_av.shape)
# print(peturb.shape)
# print(temp_diff.shape)

# %%
t_flux = t_ens_av*w_ens_av
perturb_flux = w_perturb* t_perturb

# %%
index=np.searchsorted(z,400.)
flux_400=t_flux[index]
perturb_flux_400 = perturb_flux[index,:,:]

# %%

# %%
fig,ax=plt.subplots(1,1,figsize=(10,8))
with Dataset(case_name,'r') as ncin:
    x=ncin.variables['x'][...]
    y=ncin.variables['y'][...]
cs=ax.pcolormesh(x,y,perturb_flux_400)
cb=fig.colorbar(cs)
cb.set_label('temperature flux (K/m2)',rotation=-90)

# %% [markdown]
# ## b) Plot horizontally averaged vertical temperature-flux vs. height for each of the 10 ensemble members

# %%
#ensemble=['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10']
with Dataset(case_name,'r') as ncin:
    #
    # grab the group variables
    # and plot temp flux vs. height
    # for each ens. member
    #
    fig,ax=plt.subplots(1,1,figsize=(10,8))
    for c in ensemble:
        group = ncin.groups[c]
        temp=group.variables['TABS'][-1,...] # this is for the last time step
        w =group.variables['W'][-1,...]
        t_hz_av, t_hz_p = do_reynolds(temp) # average + perturbed
        w_hz_av, w_hz_p = do_reynolds(w)
        z=ncin.variables['z'][...]
        hz_flux= (t_hz_p*w_hz_p).mean(axis=(2,1))
        ax.plot(hz_flux, z)


out=ax.set(xlabel='Temp flux (K/m2)',ylabel='height (m)',
       title=f'LES dry run for all ensemble members:  surface flux=60 $W\,m^{-2}$, $\Gamma$=10 K/km')
ax.grid(True, which='both')


# %% [markdown]
# ## Notes from class, 17 September

# %%
# edit since handing in:


group_names = list(nc_in.groups.keys()) # this will get the names of the ensemble members in this case
