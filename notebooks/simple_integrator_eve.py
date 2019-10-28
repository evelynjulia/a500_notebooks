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

# %%
def tend(y, t, F0, gamma, rho_star, wh, Cp):
    
    """
    y = intial h, initial theta, del theta
    zf = flux level height
    zh = mid-layer heights
    t = time
    l = Blackadar lengthscale at heights z(2)-z(nz)
    """
    
    g = 9.8
    
    y[0] = (k*F0) / (rho_star*Cp*y[1]) +wh

    y[1] = ((1+k)*F0) / (y[0]*Cp* rho_star)
    
    y[2] = (y[0] - wh)*gamma - y[1]
    

    return y[0],y[1],y[2]


# %%

Hs0 = 300. # surface sensible heat flux
the_lambda = 100. # used in calculating the blackadar length scale


# calculations from constants



# set up the environment
ztop = 1000. # height of fi
dz = 10. # change in height level


#length scale for the environment


# set time
tf = 3*3600 # final time length
dtout = 600 # interval length of time that we're using
tspan = np.arange(0.,tf,dtout) # create a time span array to integrate over


# calculate the mid-layer heights for which to calculate the theta value as opposed to the flux values



# choose an intial theta value for each mid-layer level
theta_i = 290 + 0.01*zh
#theta_i = 290 + 0.01*zf


# the number of half levels 
nz = len(zh) # this is 99 (because we have 100 levels)


# %%
#initial values:
yi = [5,290, 1]

# %%

# %%
# Constants
rho_star = 1.2
Cp = 1004.
k = 0.4
gamma = 10/1000 # K/m
F0 = 60
zf = np.arange(0.,ztop,dz)
zh = np.arange(dz/2,(ztop-dz/2),dz)
l = the_lambda/(1 + the_lambda/(k*zf[1:-1])) # Blackadar master lengthscale
wh = -0.01 # this is the subsidence rate ... try for different values

# %%

the_prof=integrate.odeint(tend, yi, tspan,(F0, gamma, rho_star, wh, Cp))

# y = intial h, initial theta, del theta

# %%
plt.plot(the_prof[0])


# %%
# plt.close('all')
# fig,ax = plt.subplots(1,1,figsize=(8,8))
# for item in the_prof:
#     ax.plot(item,zh)
#     ax.set_ylabel("mid-layer height")
#     ax.set_xlabel("theta")
# plt.show()

# %%
zf

# %%
x=np.empty_like(zf)
x[:]=1

# %%
# y = intial h, initial theta, del theta

# where height in zf < y[0], 
# x = y[1]
# where height in zf = y[0],
# then have a jump..  don't know how to plot that
# where height in zf > y[0],
# x = y[2]

# %%
ind = 0

for line in the_prof:
for i in zf:
    if i < y[0]:
        x[ind] = y[1]
    elif i > y[0]:


# %%
the_prof[1]

# %%
for line in the_prof:
    print(line)

# %%
