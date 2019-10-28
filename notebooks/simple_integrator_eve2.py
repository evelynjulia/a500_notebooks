# %% [markdown]
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Integrate-$\theta_v$-wrt-to-time-using-scipy.integrate" data-toc-modified-id="Integrate-$\theta_v$-wrt-to-time-using-scipy.integrate-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Integrate $\theta_v$ wrt to time using scipy.integrate</a></span></li></ul></div>

# %% [markdown]
# # Integrate $\theta_v$ wrt to time using scipy.integrate

# %%
import numpy as np
import pdb
import scipy.integrate as integrate
from matplotlib import pyplot as plt

# %% [markdown]
#

# %%
def tend(theta, t, zf, zh, l, F0, gamma, rho_star, wh, Cp):
    
    """
    zf = flux level height
    zh = mid-layer heights
    t = time
    l = Blackadar lengthscale at heights z(2)-z(nz)
    """
    
    F_theta=np.empty_like(zf) # create an array that is zf long (eg. 100 here)
    g = 9.8
    theta_av = np.mean(theta)
    dtheta_dz = np.diff(theta)/np.diff(zh)

    dbdz = (g/theta_av)*dtheta_dz # buoyancy
    dbdz[dbdz>0] = 0
    K = l**2.*np.sqrt(-16*dbdz)
    F_theta[1:-1] = -K*dtheta_dz
    F_theta[0] = F0
    F_theta[-1] = 0
    
    
    dtheta_dt = -np.diff(F_theta)/np.diff(zf)
    
    #old version
    dh_dt = (k*F_theta) / (rho_star*Cp*theta_av) +wh
    #dh_dt = (k*F0) / (rho_star*Cp*theta_av) +wh
    
    
    # dtheta_dt = (k*F_theta) / theta_av + wh*Cp*rho_star
    #dtheta_dt = ((1+k)*F_theta) / (dh_dt*Cp* rho_star)
    #dtheta_dt = ((1+k)*F0) / (dh_dt*Cp* rho_star)
    
    d_tend_dt = (dh_dt[1:] - wh)*gamma - dtheta_dt
    
    
    
#     # new version
#     dh_dt = (k*F_theta) / (rho_star*Cp*theta_av) +wh
#     h = np.diff(dh_dt)/np.diff(zf)
#     d_tend_dt = (h - wh)*gamma - dtheta_dt
    ####
    

    out = d_tend_dt
    return out
    #return d_tend_dt

# %% [markdown]
#

# %% [markdown]
#  Input parameters and theta profile (thetai):
#  Use evenly spaced flux levels from 0-ztop m with spacing dz, with 
#  initial theta given at half-levels zh. the_lambda is the asymptotic Blackadar 
#  lengthscale, and Hs0 is the surface sensible heat flux (W/m2)

# %%
# Constants
rho_star = 1.2
Cp = 1004.
k = 0.4
gamma = 10/1000 # K/m 
Hs0 = 300. # surface sensible heat flux
the_lambda = 100. # used in calculating the blackadar length scale
wh = 10 # this is the subsidence rate ... try for different values

# calculations from constants
F0 = Hs0/(rho_star*Cp)


# set up the environment
ztop = 1000. # height of fi
dz = 10. # change in height level
zf = np.arange(0.,ztop,dz)

#length scale for the environment
l = the_lambda/(1 + the_lambda/(k*zf[1:-1])) # Blackadar master lengthscale

# set time
tf = 3*3600 # final time length
dtout = 600 # interval length of time that we're using
tspan = np.arange(0.,tf,dtout) # create a time span array to integrate over


# calculate the mid-layer heights for which to calculate the theta value as opposed to the flux values
zh = np.arange(dz/2,(ztop-dz/2),dz)


# choose an intial theta value for each mid-layer level
theta_i = 290 + 0.01*zh
#theta_i = 290 + 0.01*zf


# the number of half levels 
nz = len(zh) # this is 99 (because we have 100 levels)



# %%

# %%

# %%
# %matplotlib 

# %%
# def tend(theta, t, zf, zh, l, F0, gamma, rho_star, wh, Cp):


the_prof=integrate.odeint(tend, theta_i, tspan,(zf, zh, l, F0, gamma, rho_star, wh, Cp))
plt.close('all')
fig,ax = plt.subplots(1,1,figsize=(8,8))
for item in the_prof:
    ax.plot(item,zh)
    ax.set_ylabel("mid-layer height")
    ax.set_xlabel("theta")
plt.show()

# %%

# %%

# %%
