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
# # Chapter 6 questions

# %% [markdown]
# ## Question 14

# %%
import matplotlib.pyplot as plt
import numpy as np

# %%
z = [80,70,60,50,40,30,20,10,0] # m
theta_v = [305,305,301,300,298,294,292,292,293] # K
U = [18,17,15,14,10,8,7,7,2] # m/s

# %%
fig,ax=plt.subplots(1,2,figsize=(18,5))
ax[0].plot(theta_v, z);
ax[0].set(xlabel=r'$\overline{\theta}$ (K)',ylabel='height (m)',
       title = '');
ax[1].plot(U,z);
ax[1].set(xlabel=r'$\overline{U}$ (m/s)',ylabel='height (m)',
       title = '');

# %%
K = 5 # m^2/s

# %%
# a) u'w'

dUdz = -np.diff(U)/-np.diff(z)

a = -K*dUdz
print(z)
print(a)

# b) w'theta_v'
dtheta_vdz = -np.diff(theta_v)/-np.diff(z)
b = -1.35*K*dtheta_vdz
print(b)

# %%
fig,ax=plt.subplots(1,2,figsize=(18,5))
ax[0].plot(a, z[1:]);
ax[0].set(xlabel=r"$\overline{u'w'}$",ylabel='height (m)',
       title = '');
ax[1].plot(b, z[1:]);
ax[1].set(xlabel=r"$\overline{w'\theta}$'",ylabel='height (m)',
       title = '');

#r'$\overline{\theta}$ (K)'

# %%
np.mean(theta_v)

# %%

# %%

# %%

# %%
