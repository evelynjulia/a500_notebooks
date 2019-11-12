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
# <div class="toc"><ul class="toc-item"></ul></div>

# %%
import context
from a500.thermlib import thermfuncs as tf
import a500.thermlib as thermlib
import pandas as pd

Temp=280. #K
press=90. #kPa
#
# find the saturation mixing ratio and potential temp from the temperature and pressure
#
print(tf.qs_tp(Temp,press))
print(tf.theta(Temp,press))
#
# find the dew point temperature and the lifting condensation level
#
psurf=100.  #kPa
Tsurf=290.
qvap=7.e-3  #kg/kg
Tdew = tf.tmr(qvap,psurf)
print('the surface dew point temp is: ',Tdew)
LCL = tf.LCL(Tdew,Tsurf,psurf)
print('the LCL is {:5.2f} kPa'.format(LCL))

#
# find thetal 
#
thetal = tf.alt_thetal(psurf,Tsurf,qvap)
#
# invert thetal for temperature, vapor, liquid
#
print(tf.t_uos_thetal(thetal,qvap,80.))
#
# make a sounding
#
press_levs=np.linspace(80,100.,20.)
press_levs=press_levs[::-1]
sounding=[]
for press in press_levs:
    sounding.append(tf.t_uos_thetal(thetal,qvap,press))
    
df_sounding=pd.DataFrame.from_records(sounding)

# %%
from matplotlib import pyplot as plt
# %matplotlib inline
fig,ax = plt.subplots(1,2,figsize=(12,8))
ax[0].plot(df_sounding['RV']*1.e3,press_levs)
ax[0].invert_yaxis()
ax[1].plot(df_sounding['RL']*1.e3,press_levs)
ax[1].invert_yaxis()
ax[0].set(title='vapor mixing ratio',xlabel='qv (g/kg)',ylabel='pressure (kPa)')
out=ax[1].set(title='liquid mixing ratio',xlabel='ql (g/kg)',ylabel='pressure (kPa)')

# %%
