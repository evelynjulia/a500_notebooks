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
thta_intp = interpolate.interp1d(df['PRESS'].values, df['THTA'].values)
new_heights = np.arange(42,2500,10)
comp_thta = thta_intp(new_heights)


fig, ax = plt.subplots()
ax.plot(comp_thta, new_heights, '.-')
ax.plot(df['THTA'], df['HGHT'], '.-')
plt.show()

# PRES   HGHT  TEMP  DWPT  RH  MIXR  WDIR  WSPD   THTA   THTE   THTV        DATE

# pres_vals = ['PRES_200mb', 'PRES_250mb', 'PRES_500mb', 'PRES_700mb', 'PRES_850mb', 'PRES_925mb', 'PRES_1000mb']
p_levs = [1000, 925, 850, 700, 500, 250, 200]

df_all = pd.DataFrame()


for file in list_of_files[0:1]:
    df = pd.read_csv(file, index_col= 'Unnamed: 0')
    date_i = os.path.basename(file)[0:len_date]
    print(df)
    new_df_i = pd.DataFrame()
    # now we have the df
    if df.shape[0] > 0:
        # get interpolations for new columns
        thta_intp = interpolate.interp1d(df['PRES'].values, df['THTA'].values)
        hght_intp = interpolate.interp1d(df['PRES'].values, df['HGHT'].values)

        # then add the columns to a new df
        new_df_i['PRES'] = p_levs
        new_df_i['THTA'] = thta_intp(p_levs)
        new_df_i['HGHT'] = hght_intp(p_levs)
        new_df_i['DATE'] = df['DATE']
        
        # calc gradient (dtheta_dp)
        # need to make it negative because pressure decreases with height
        new_df_i['THTA_GRAD'] = - np.gradient(new_df_i['THTA'], new_df_i['PRES'])

        # create column for stability class
        # 0.005 should be about a 0.5 deg C change in temp from 1000mb to 925mb
        if new_df_i['THTA_GRAD'][0] >= 0.005:
            new_df_i['STABILITY'] = 1 # stable
        elif new_df_i['THTA_GRAD'][0] < 0.005 and new_df_i['THTA_GRAD'][0] > -0.05:
            new_df_i['STABILITY'] = 0 # neutral
        elif new_df_i['THTA_GRAD'][0] <= -0.005:
            new_df_i['STABILITY'] = -1 # unstable
        else:
            print('None of the conditions were met. Maybe check this for date')
        
        # Column for wind cat

        # column for day / night
        if new_df_i['DATE'][0] >= 0.005:

        # add new df to a list of all dataframes
        print(new_df_i)
    
    else: 
        print(date_i,' sounding dataframe is empty... skipping this date/time.')






fig, ax = plt.subplots()
ax.plot(new_df_i['THTA'],p_levs,  '.-')
#ax.plot(df['THTA'], df['HGHT'], '.-')
ax.invert_yaxis()
plt.show()







# add to loop after
        
        # add to all one df
        df_all = df_all.append(df)
        print('Adding data for ', date_i)
        print(df_all.shape)
    else: 
        print(date_i,' sounding dataframe is empty... skipping this date/time.')
