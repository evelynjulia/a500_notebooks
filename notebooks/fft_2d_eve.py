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
#     sideBar: true
#     skip_h1_title: false
#     title_cell: Table of Contents
#     title_sidebar: Contents
#     toc_cell: true
#     toc_position:
#       height: calc(100% - 180px)
#       left: 10px
#       top: 150px
#       width: 256px
#     toc_section_display: true
#     toc_window_display: true
# ---

# %% [markdown] {"toc": true}
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#2D-histogram-of-the-optical-depth-$\tau$" data-toc-modified-id="2D-histogram-of-the-optical-depth-$\tau$-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>2D histogram of the optical depth $\tau$</a></span><ul class="toc-item"><li><span><a href="#Character-of-the-optical-depth-field" data-toc-modified-id="Character-of-the-optical-depth-field-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Character of the optical depth field</a></span></li><li><span><a href="#ubc_fft-class" data-toc-modified-id="ubc_fft-class-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>ubc_fft class</a></span></li><li><span><a href="#Designing-a-filter" data-toc-modified-id="Designing-a-filter-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Designing a filter</a></span></li></ul></li><li><span><a href="#Homework" data-toc-modified-id="Homework-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Homework</a></span><ul class="toc-item"><li><span><a href="#With-a-rectanguler-filter" data-toc-modified-id="With-a-rectanguler-filter-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>With a rectanguler filter</a></span><ul class="toc-item"><li><span><a href="#Calculate-filter-function,-filtered-fft,-and-reverse-fft" data-toc-modified-id="Calculate-filter-function,-filtered-fft,-and-reverse-fft-2.1.1"><span class="toc-item-num">2.1.1&nbsp;&nbsp;</span>Calculate filter function, filtered fft, and reverse fft</a></span></li><li><span><a href="#Plot-filter" data-toc-modified-id="Plot-filter-2.1.2"><span class="toc-item-num">2.1.2&nbsp;&nbsp;</span>Plot filter</a></span></li><li><span><a href="#Plot-filtered-and-non-filtered-fft-for-one-row" data-toc-modified-id="Plot-filtered-and-non-filtered-fft-for-one-row-2.1.3"><span class="toc-item-num">2.1.3&nbsp;&nbsp;</span>Plot filtered and non-filtered fft for one row</a></span></li><li><span><a href="#Plot-back-transformed-filtered-data" data-toc-modified-id="Plot-back-transformed-filtered-data-2.1.4"><span class="toc-item-num">2.1.4&nbsp;&nbsp;</span>Plot back transformed filtered data</a></span></li></ul></li><li><span><a href="#Now-with-a-circular-filter" data-toc-modified-id="Now-with-a-circular-filter-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Now with a circular filter</a></span><ul class="toc-item"><li><span><a href="#Plot-filter" data-toc-modified-id="Plot-filter-2.2.1"><span class="toc-item-num">2.2.1&nbsp;&nbsp;</span>Plot filter</a></span></li><li><span><a href="#Plot-back-transformed-filtered-data" data-toc-modified-id="Plot-back-transformed-filtered-data-2.2.2"><span class="toc-item-num">2.2.2&nbsp;&nbsp;</span>Plot back transformed filtered data</a></span></li></ul></li><li><span><a href="#Original-vs-filtered" data-toc-modified-id="Original-vs-filtered-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>Original vs filtered</a></span></li></ul></li></ul></div>

# %% [markdown] {"collapsed": true}
# # 2D histogram of the optical depth $\tau$
#
# Below I calculate the 2-d and averaged 1-d spectra for the optical depth, which gives the penetration
# depth of photons through a cloud, and is closely related to cloud thickness. Follows
# [Lewis et al., 2004](http://onlinelibrary.wiley.com/doi/10.1029/2003JD003742/full)

# %%
from pathlib import Path
import warnings
warnings.filterwarnings("ignore",category=FutureWarning)
import context

# %%
from matplotlib import pyplot as plt
import urllib
import os
from a500.utils.data_read import download

data_download=True
satfile='a17.nc'
download(satfile,root='http://clouds.eos.ubc.ca/~phil/docs/atsc500/data',
        dest_folder=context.data_dir)

# %%
from netCDF4 import Dataset
from a500.utils.ncdump import ncdump
with Dataset(context.data_dir / satfile) as nc:
    #ncdump(nc)
    tau=nc.variables['tau'][...]

# %%
tau.shape

# %% [markdown]
# ## Character of the optical depth field
#
# The image below shows one of the marine boundary layer landsat scenes analyzed in 
# [Lewis et al., 2004](http://onlinelibrary.wiley.com/doi/10.1029/2003JD003742/full)
#
# It is a 2048 x 2048 pixel image taken by Landsat 7, with the visible reflectivity converted to
# cloud optical depth.   The pixels are 25 m x 25 m, so the scene extends for about 50 km x 50 km

# %%
# %matplotlib inline
from mpl_toolkits.axes_grid1 import make_axes_locatable
plt.close('all')
fig,ax=plt.subplots(1,2,figsize=(13,7))
ax[0].set_title('landsat a17')
im0=ax[0].imshow(tau)
im1=ax[1].hist(tau.ravel())
ax[1].set_title('histogram of tau values')
divider = make_axes_locatable(ax[0])
cax = divider.append_axes("bottom", size="5%", pad=0.35)
out=fig.colorbar(im0,orientation='horizontal',cax=cax)

# %% [markdown]
# ## ubc_fft class

# %% [markdown]
# In the next cell I define a class that calculates the 2-d fft for a square image
#
# in the method ```power_spectrum``` we calculate both the 2d fft and the power spectrum
# and save them as class attributes.  In the method ```annular_average``` I take the power spectrum,
# which is the two-dimensional field  $E(k_x, k_y)$ (in cartesian coordinates) or $E(k,\theta)$ (in polar coordinates).
# In the method ```annular_avg``` I take the average
#
# $$
# \overline{E}(k) = \int_0^{2\pi} E(k, \theta) d\theta
# $$
#
# and plot that average with the method ```graph_spectrum```

# %%
from netCDF4 import Dataset
import numpy as np
import math
from numpy import fft
from matplotlib import pyplot as plt


class ubc_fft:

    def __init__(self, filename, var, scale):
        """
        
            Parameters
            -----------
            
            filename: string or Path
               full path to file
            varname: string
               netcdf variable name
            scale: float
               size of pixel in km

           Constructer opens the netcdf file, reads the data and
           saves the twodimensional fft
        """
        filename = Path(filename)
        with Dataset(filename,'r') as fin:
            data = fin.variables[var][...]
        data = data - data.mean()
        if data.shape[0] != data.shape[1]:
            raise ValueError('expecting square matrix')
        self.xdim = data.shape[0]     # size of each row of the array
        self.midpoint = int(math.floor(self.xdim/2))
        self.filename = filename.stem
        self.var = var
        self.scale = float(scale)
        self.data = data
        self.fft_data = fft.fft2(self.data)
    
    def power_spectrum(self):
        """
           calculate the power spectrum for the 2-dimensional field
        """
        #
        # fft_shift moves the zero frequency point to the  middle
        # of the array  
        #
        fft_shift = fft.fftshift(self.fft_data)
        spectral_dens = fft_shift*np.conjugate(fft_shift)/(self.xdim*self.xdim)
        spectral_dens = spectral_dens.real
        #
        # dimensional wavenumbers for 2dim spectrum  (need only the kx
        # dimensional since image is square
        #
        k_vals = np.arange(0,(self.midpoint))+1
        k_vals = (k_vals-self.midpoint)/(self.xdim*self.scale)
        self.spectral_dens=spectral_dens
        self.k_vals=k_vals

    def annular_avg(self,avg_binwidth):
        """ 
         integrate the 2-d power spectrum around a series of rings 
         of radius kradial and average into a set of 1-dimensional
         radial bins
        """
        #
        #  define the k axis which is the radius in the 2-d polar version of E
        #
        numbins = int(round((math.sqrt(2)*self.xdim/avg_binwidth),0)+1)

        avg_spec = np.zeros(numbins,np.float64)
        bin_count = np.zeros(numbins,np.float64)

        print("\t- INTEGRATING... ")
        for i in range(self.xdim):
            if (i%100) == 0:
                print("\t\trow: {} completed".format(i))
            for j in range(self.xdim):
                kradial = math.sqrt(((i+1)-self.xdim/2)**2+((j+1)-self.xdim/2)**2)
                bin_num = int(math.floor(kradial/avg_binwidth))
                avg_spec[bin_num]=avg_spec[bin_num]+ kradial*self.spectral_dens[i,j]
                bin_count[bin_num]+=1

        for i in range(numbins):
            if bin_count[i]>0:
                avg_spec[i]=avg_spec[i]*avg_binwidth/bin_count[i]/(4*(math.pi**2))
        self.avg_spec=avg_spec
        #
        # dimensional wavenumbers for 1-d average spectrum
        #
        self.k_bins=np.arange(numbins)+1
        self.k_bins = self.k_bins[0:self.midpoint]
        self.avg_spec = self.avg_spec[0:self.midpoint]

        
    
    def graph_spectrum(self, kol_slope=-5./3., kol_offset=1., \
                      title=None):
        """
           graph the annular average and compare it to Kolmogorov -5/3
        """
        avg_spec=self.avg_spec
        delta_k = 1./self.scale                # 1./km (1/0.025 for landsat 25 meter pixels)
        nyquist = delta_k * 0.5
        knum = self.k_bins * (nyquist/float(len(self.k_bins)))# k = w/(25m)
        #
        # draw the -5/3 line through a give spot
        #
        kol = kol_offset*(knum**kol_slope)
        fig,ax=plt.subplots(1,1,figsize=(8,8))
        ax.loglog(knum,avg_spec,'r-',label='power')
        ax.loglog(knum,kol,'k-',label="$k^{-5/3}$")
        ax.set(title=title,xlabel='k (1/km)',ylabel='$E_k$')
        ax.legend()
        self.plotax=ax


# %%
output = ubc_fft(context.data_dir / satfile,'tau',0.025)
output.power_spectrum()

# %%
fig,ax=plt.subplots(1,1,figsize=(7,7))
ax.set_title('landsat a17')
im0=ax.imshow(np.log10(output.spectral_dens))
ax.set_title('log10 of the 2-d power spectrum')
divider = make_axes_locatable(ax)
cax = divider.append_axes("bottom", size="5%", pad=0.35)
out=fig.colorbar(im0,orientation='horizontal',cax=cax)

# %%
do_avg = True
if do_avg:
    avg_binwidth=5  #make the kradial bins 5 pixels wide
    output.annular_avg(avg_binwidth)

# %%
output.graph_spectrum(kol_offset=2000.,title='Landsat {} power spectrum'.format(output.filename))

# %%
2/0.0195

# %% [markdown] {"trusted": true}
# ## Designing a filter
#
# We've got a very similar situation to the fftnotebook.py example, except that rather than oscilating in time for a fixed
# location, our Fourier modes are oscillating in space for a fixed time. For spatial oscilations, the equivalent of the frequency
# in units of 1/time is the wavenumber, in units of 1/length. Instead of sampling 20.833 time per second, we are
# sampling 1000./25 = 40 times per kilometer, i.e our wavenumber sampling rate is 40 $km^{-1}$.  What is the bin resolution
# of our sample?  We have 2048 bins in each direction, so each bin represents 40/2048 = 0.0195 $km^{-1}$.  Suppose we want to
# filter out all wavenumbers greater than 1/(0.5 km) = 2 $km^{-1}$?  The bin we need to use in our slice is bin 2/0.0195 = index 102 

# %%

# %% [markdown]
# # Homework

# %% [markdown]
# Modify `fft_2d.py` to filter out all fluctuations with length scales smaller than 2 km. Show images of your filter, the filtered fft and the transformed filtered image.

# %% [markdown]
# ## With a rectanguler filter

# %% [markdown]
# ### Calculate filter function, filtered fft, and reverse fft

# %%
totsize = output.xdim
samprate=1000/25 #per km

# now we want to filter out 2 waves per km
filt = 2

bin_width=samprate/(totsize)
print('bin width = ', bin_width)
k2_index=int(np.floor(filt/bin_width))
print('2km bin index = ', k2_index)

filter_func=np.ones_like(output.fft_data,dtype=np.float64)
filter_func[:,k2_index:-k2_index]=0.

# filter_func=np.zeros_like(output.fft_data,dtype=np.float64)
# filter_func[:,k2_index:-k2_index]=1.
#filter_func[k2_index:-k2_index,k2_index:-k2_index]=0.

#print('filter function shape = ',filter_func.shape)
#print('filter function = ', filter_func)

#--------------------------------------------
# calculate filtered fft and filtered power:

filt_fft = filter_func*output.fft_data
#Power=np.real(thefft*np.conj(thefft))
filt_power=np.real(filt_fft*np.conj(filt_fft))



#--------------------------------------------
# do an inverse fft to get back data in the orignal space

filt_back_data=np.real(np.fft.ifft2(filt_fft))
#filt_data=np.real(np.fft.ifft2(filter_func*output.fft_data)) 

# %% [markdown]
# ### Plot filter

# %%
plt.imshow(filter_func)

# %%

# %%
# # do the fft

# # on the results let anything smaller than the index = 0

# fig,ax=plt.subplots(1,1,figsize=(7,7))
# ax.set_title('landsat a17')
# im0=ax.imshow(np.log10(filter_func))
# #im0=ax.imshow(filter_func)
# #ax.set_title('log10 of the 2-d power spectrum')
# divider = make_axes_locatable(ax)
# cax = divider.append_axes("bottom", size="5%", pad=0.35)
# out=fig.colorbar(im0,orientation='horizontal',cax=cax)

# %%
# # # %matplotlib inline
# from mpl_toolkits.axes_grid1 import make_axes_locatable
# plt.close('all')
# fig,ax=plt.subplots(1,2,figsize=(13,7))
# ax[0].set_title('real - filtered fft data')
# im0=ax[0].imshow(np.log10(filt_data))
# #im1=ax[1].hist(filt_data.ravel())
# #ax[1].set_title('histogram of tau values')
# divider = make_axes_locatable(ax[0])
# cax = divider.append_axes("bottom", size="5%", pad=0.35)
# out=fig.colorbar(im0,orientation='horizontal',cax=cax)



# %%
#plot filtered fft data

# fig,ax=plt.subplots(1,1,figsize=(7,7))
# ax.set_title('fft - power')
# im0=ax.imshow(np.log10(filt_power))
# #ax.set_title('log10 of the 2-d power spectrum')
# divider = make_axes_locatable(ax)
# cax = divider.append_axes("bottom", size="5%", pad=0.35)
# out=fig.colorbar(im0,orientation='horizontal',cax=cax)


# %%
# fig,ax=plt.subplots(1,1,figsize=(7,7))
# ax.set_title('landsat a17')
# #im0=ax.imshow(np.log10(filter_func))
# im0=ax.imshow(np.log10(np.real(output.fft_data)))
# ax.set_title('real - Original fft data')
# divider = make_axes_locatable(ax)
# cax = divider.append_axes("bottom", size="5%", pad=0.35)
# out=fig.colorbar(im0,orientation='horizontal',cax=cax)

# %% [markdown]
# ### Plot filtered and non-filtered fft for one row

# %%
#filt_power.shape
#plt.plot(filt_power[200,:])
#filt_fft[200,:].shape

fig,ax=plt.subplots(1,1,figsize=(9,5))
ax.plot(output.fft_data[200,:], label = 'fft')
ax.plot(filt_fft[200,:], label = 'filtered fft')
ax.legend()

#plt.plot(filt_power[200,:])

# %%

# %% [markdown] {"trusted": true}
# ### Plot back transformed filtered data

# %%
plt.close('all')
fig,ax=plt.subplots(1,2,figsize=(13,7))
ax[0].set_title('filtered back data')
im0=ax[0].imshow(np.log10(filt_back_data))
#im0=ax[0].imshow(filt_back_data)
im1=ax[1].hist(filt_back_data.ravel())
ax[1].set_title('histogram of tau values')
divider = make_axes_locatable(ax[0])
cax = divider.append_axes("bottom", size="5%", pad=0.35)
out=fig.colorbar(im0,orientation='horizontal',cax=cax)


# %%

# %%
#output.xdim # size of each row of the array
#output.midpoint
#output.filename 
#output.var 
#output.scale 
#output.data 
#output.fft_data 
#output.spectral_dens
#output.k_vals
#output.avg_spec

# %%

# %% [markdown] {"trusted": true}
# ## Now with a circular filter
#

# %%
def sector_mask(shape,centre,radius,angle_range):
    """
    Return a boolean mask for a circular sector. The start/stop angles in  
    `angle_range` should be given in clockwise order.
    """

    x,y = np.ogrid[:shape[0],:shape[1]]
    cx,cy = centre
    tmin,tmax = np.deg2rad(angle_range)

    # ensure stop angle > start angle
    if tmax < tmin:
            tmax += 2*np.pi

    # convert cartesian --> polar coordinates
    r2 = (x-cx)*(x-cx) + (y-cy)*(y-cy)
    theta = np.arctan2(x-cx,y-cy) - tmin

    # wrap angles between 0 and 2*pi
    theta %= (2*np.pi)

    # circular mask
    circmask = r2 <= radius*radius

    # angular mask
    anglemask = theta <= (tmax-tmin)

    return circmask*anglemask


# %%
rad_filter_func=np.zeros_like(output.fft_data,dtype=np.float64)
mask = sector_mask(rad_filter_func.shape,(output.midpoint,output.midpoint),973,(0,360))
rad_filter_func[~mask] = 1
#rad_filter_func[:,k2_index:-k2_index]=0.

# %% [markdown]
# ### Plot filter

# %%
plt.imshow(rad_filter_func);

# %%
rad_filt_fft = rad_filter_func*output.fft_data
#Power=np.real(thefft*np.conj(thefft))
rad_filt_power=np.real(rad_filt_fft*np.conj(rad_filt_fft))

#--------------------------------------------
# do an inverse fft to get back data in the orignal space

rad_filt_back_data=np.real(np.fft.ifft2(rad_filt_fft))

# %% [markdown]
# ### Plot back transformed filtered data

# %%
fig,ax=plt.subplots(1,2,figsize=(13,7))
ax[0].set_title('filtered back data')
im0=ax[0].imshow(rad_filt_back_data)
#im0=ax[0].imshow(filt_back_data)
im1=ax[1].hist(rad_filt_back_data.ravel())
ax[1].set_title('histogram of tau values')
divider = make_axes_locatable(ax[0])
cax = divider.append_axes("bottom", size="5%", pad=0.35)
out=fig.colorbar(im0,orientation='horizontal',cax=cax)

# %% [markdown]
# ## Original vs filtered

# %%
fig,ax=plt.subplots(1,2,figsize=(13,7))
ax[0].set_title('Original data')
im0=ax[0].imshow(tau)
im1=ax[1].imshow(rad_filt_back_data)
ax[1].set_title('Filtered data')
divider = make_axes_locatable(ax[0])

cax = divider.append_axes("bottom", size="5%", pad=0.35)
out=fig.colorbar(im0,orientation='horizontal',cax=cax)
#out=fig.colorbar(im1,orientation='horizontal',cax=cax)

# %%
