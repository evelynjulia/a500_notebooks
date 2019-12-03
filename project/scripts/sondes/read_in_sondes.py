# Eve Wicksteed
#
# 23 November 2019

import glob
#from netCDF4 import Dataset
import numpy as np
import datetime as dt
#from a500.utils import ncdump
#from netCDF4 import num2date, date2num
import pandas as pd
import os
import matplotlib.pyplot as plt

import pickle


data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'

list_of_files = glob.glob('/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/*.csv')

len_date = 10

# read all into one dataframe and then groupby date
fig, ax = plt.subplots()
fig2, ax2 = plt.subplots()

df_all = pd.DataFrame()
for file in list_of_files[0:50]:
    df = pd.read_csv(file, index_col= 'Unnamed: 0')
    date_i = os.path.basename(file)[0:len_date]
    if df.shape[0] > 0:
        # PLOT
        ax.plot(df['THTA'][df['HGHT'] < 2500], df['HGHT'][df['HGHT'] < 2500], '.-', label = date_i)
        ax2.plot(df['WSPD'][df['HGHT'] < 2500], df['HGHT'][df['HGHT'] < 2500], '.-', label = date_i)
        # add to all one df
        df_all = df_all.append(df)
        print('Adding data for ', date_i)
        print(df_all.shape)
    else: 
        print(date_i,' sounding dataframe is empty... skipping this date/time.')


ax.set_ylabel('Height')
ax.set_xlabel('Theta')
ax2.set_ylabel('Height')
ax2.set_xlabel('Wind speed')
#plt.legend()
plt.show()



###
# to get only the bottom values
df_all[df_all['PRES']>= 900]



############################################################
# test - not with plotting, just in creating DF

from scipy import interpolate

# 
df_all = pd.DataFrame()
for file in list_of_files[0:1]:
    df = pd.read_csv(file, index_col= 'Unnamed: 0')
    date_i = os.path.basename(file)[0:len_date]
    print(df)


# this works for interpolation
thta_intp = interpolate.interp1d(df['HGHT'].values, df['THTA'].values)
new_heights = np.arange(42,2500,10)
comp_thta = thta_intp(new_heights)


fig, ax = plt.subplots()
ax.plot(comp_thta, new_heights, '.-')
ax.plot(df['THTA'], df['HGHT'], '.-')
plt.show()

# PRES   HGHT  TEMP  DWPT  RH  MIXR  WDIR  WSPD   THTA   THTE   THTV        DATE

df_all = pd.DataFrame()
for file in list_of_files[0:1]:
    df = pd.read_csv(file, index_col= 'Unnamed: 0')
    date_i = os.path.basename(file)[0:len_date]
    print(df)
    if df.shape[0] > 0:
        # add to all one df
        df_all = df_all.append(df)
        print('Adding data for ', date_i)
        print(df_all.shape)
    else: 
        print(date_i,' sounding dataframe is empty... skipping this date/time.')
