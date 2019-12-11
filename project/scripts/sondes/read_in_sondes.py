#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
from scipy import interpolate

import pickle


data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'

#list_of_files = sorted(glob.glob('/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/*.csv'))
list_of_files = glob.glob('/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/*.csv')

# params / constants
len_date = 10
top_pres = 850
stability_limit = 0.005 # what the cutoff is K/mb



# read all into one dataframe and then groupby date
fig, ax = plt.subplots()
# fig2, ax2 = plt.subplots()

df_all = pd.DataFrame()
for file in list_of_files[1:20]:
    df = pd.read_csv(file, index_col= 'Unnamed: 0')
    date_i = os.path.basename(file)[0:len_date]
    if df.shape[0] > 0:
        # PLOT
        ax.plot(df['THTA'][df['PRES'] > top_pres], df['HGHT'][df['PRES'] > top_pres], '.-', label = date_i)
        #ax2.plot(df['WSPD'][df['PRES'] > top_pres], df['PRES'][df['PRES'] > top_pres], '.-', label = date_i)
        # add to all one df
        #ax.plot(df['THTA'][0:10], df['HGHT'][0:10], '.-', label = date_i)
        df_all = df_all.append(df)
        print('Adding data for ', date_i)
        print(df_all.shape)
        # df['THTA_GRAD'] = np.gradient(df['THTA'], df['PRES'])
        # df['mean_grad'] = np.mean(df['THTA_GRAD'][df['PRES'] > top_pres])

        # get gradient for stability classes:
        df['THTA_GRAD'] = np.gradient(df['THTA'], df['PRES'])
        df['MEAN_GRAD'] = np.mean(df['THTA_GRAD'][df['PRES'] >= top_pres])

        # create column for stability class
        # 0.005 should be about a 0.5 deg C change in temp from 1000mb to 925mb
        stability_conditions = [
            df['THTA_GRAD'][0] >= stability_limit,
            (df['THTA_GRAD'][0] < stability_limit) & (df['THTA_GRAD'][0] > -stability_limit),
            df['THTA_GRAD'][0] <= -stability_limit]
        stability_choices = [-1, 0, 1]  #['unstable', 'neutral', 'stable']
        df['STABILITY'] = np.select(stability_conditions, stability_choices)

        print(df)
    else: 
        print(date_i,' sounding dataframe is empty... skipping this date/time.')


ax.set_ylabel('Height (m)')
ax.set_xlabel('Theta (K)')
# ax2.set_ylabel('Pressure')
# ax2.set_xlabel('Wind speed')
plt.legend()
#ax.invert_yaxis()
ax.set_title('Sounding data')
plt.show()



###
# to get only the bottom values
# df_all[df_all['PRES']>= 900]
# df = pd.read_csv(list_of_files[7], index_col= 'Unnamed: 0')
# fig, ax = plt.subplots()
# ax.plot(df['THTA'], df['HGHT'], 'r.-', linewidth=2, markersize =10)
# plt.show()
# ax.set_ylabel('Height (m)')
# ax.set_xlabel('Theta (K)')
# ax.set_title('Sounding data')



############################################################
# test - not with plotting, just in creating DF




# PRES   HGHT  TEMP  DWPT  RH  MIXR  WDIR  WSPD   THTA   THTE   THTV        DATE
#df_all = pd.DataFrame()

p_levs = [1000, 925, 850, 700, 500, 250, 200]

fig, ax = plt.subplots()


sonde_stabilty_classes = []
sonde_gradients = []

i = 0
for file in list_of_files[0:20]:
    i += 1
    print('\nnumber of files read = ',i)
    df = pd.read_csv(file, index_col= 'Unnamed: 0')
    #print(df)
    date_i = os.path.basename(file)[0:len_date]
    print(date_i)
    hr_i = date_i[-2:]
    print(hr_i)
    new_df_i = pd.DataFrame()
    # now we have the df
    if df.shape[0] > 0:
        
        # get gradient for stability classes:
        df['THTA_GRAD'] = np.gradient(df['THTA'], df['PRES'])
        df['MEAN_GRAD'] = np.mean(df['THTA_GRAD'][df['PRES'] >= top_pres])
        mean_grad_i = np.mean(df['THTA_GRAD'][df['PRES'] >= top_pres])

        # create column for stability class
        # 0.005 should be about a 0.5 deg C change in temp from 1000mb to 925mb
        # calculate stabilty from the 1000mb to 850mb (top_pres) mean

        stability_conditions = [
            df['MEAN_GRAD'][0] >= stability_limit,
            (df['MEAN_GRAD'][0] < stability_limit) & (df['MEAN_GRAD'][0] > -stability_limit),
            df['MEAN_GRAD'][0] <= -stability_limit]
        stability_choices = [-1, 0, 1]  #['unstable', 'neutral', 'stable']
        

        # get interpolations for new columns
        thta_intp = interpolate.interp1d(df['PRES'].values, df['THTA'].values)
        hght_intp = interpolate.interp1d(df['PRES'].values, df['HGHT'].values)
        
        # then add the columns to a new df
        new_df_i['PRES'] = p_levs
        try:
            new_df_i['THTA'] = thta_intp(p_levs)
        except Exception:
            print('broke loop (hopefully)')
            continue
        
        try:
            new_df_i['HGHT'] = hght_intp(p_levs)
        except Exception:
            print('broke loop (hopefully)')
            continue
        new_df_i['DATE'] = df['DATE']
        
        # calc gradient (dtheta_dp)
        # need to make it negative because pressure decreases with height
        new_df_i['THTA_GRAD_INTERP'] = - np.gradient(new_df_i['THTA'], new_df_i['PRES'])
        new_df_i['MEAN_GRAD_INTERP'] = np.mean(new_df_i['THTA_GRAD_INTERP'][new_df_i['PRES'] >= top_pres])

        


        # set column in new_df_i
        new_df_i['STABILITY'] = np.select(stability_conditions, stability_choices)
        new_df_i['MEAN_GRAD_BELOW_'+str(top_pres)] = mean_grad_i  # mean gradient below 850mb (top_pres), not interpolated

        sonde_stabilty_classes.append(new_df_i['STABILITY'][0])
        # print('Stability = ', new_df_i['STABILITY'][0])
        sonde_gradients.append(mean_grad_i)
        # print('Mean Grad = ', mean_grad_i)


        # # don't need this (section below) anymore because calculate stability for
        # # just the initial sounding data by calculating the mean of data under 850mb

        # # create column for stability class
        # # 0.005 should be about a 0.5 deg C change in temp from 1000mb to 925mb
        # stability_conditions = [
        #     new_df_i['THTA_GRAD'][0] >= 0.005,
        #     (new_df_i['THTA_GRAD'][0] < 0.005) & (new_df_i['THTA_GRAD'][0] > -0.005),
        #     new_df_i['THTA_GRAD'][0] <= -0.005]
        # stability_choices = [1, 0, -1]  #['stable', 'neutral', 'unstable']
        # new_df_i['STABILITY'] = np.select(stability_conditions, stability_choices)

        # column for day / night (Time Of Day)
        tod_conditions = [
            hr_i == '00',
            hr_i == '12']
        tod_choices = [0, 12]  #['night', 'day']
        new_df_i['TOD'] = np.select(tod_conditions, tod_choices)
        
        print(new_df_i)
        ax.plot(new_df_i['THTA'], new_df_i['PRES'], '.-', label = date_i)
        

    else: 
        print(date_i,'sounding dataframe is empty... skipping this date/time.')
    

ax.set_ylabel('Pressure (mb)')
ax.set_xlabel('Theta (K)')
# ax2.set_ylabel('Pressure')
# ax2.set_xlabel('Wind speed')
plt.legend()
ax.invert_yaxis()
ax.set_title('Sounding data')
plt.show()

# # test np where
# #new_df_i['test_npwhere'] = np.where(new_df_i['THTA_GRAD'][0] >= 0.005, 'stable', 'other')
# stability_conditions = [
#     new_df_i['THTA_GRAD'][0] >= 0.005,
#     (new_df_i['THTA_GRAD'][0] < 0.005) & (new_df_i['THTA_GRAD'][0] > -0.05),
#     new_df_i['THTA_GRAD'][0] <= -0.005]
# stability_choices = [1, 0, -1]  #['stable', 'neutral', 'unstable']
# new_df_i['STABILITY'] = np.select(stability_conditions, stability_choices)

# tod_conditions = [
#     hr_i == '00',
#     hr_i == '12']
# tod_choices = [0, 12]  #['night', 'day']
# new_df_i['TOD'] = np.select(tod_conditions, tod_choices)

# print(new_df_i)

print('stab classes',sonde_stabilty_classes)
print('gradients',sonde_gradients)




# TO DO / add to loop above
# add new df to a list of all dataframes  
# Column for wind cat

# ### PLOTTING
# fig, ax = plt.subplots()
# ax.plot(new_df_i['THTA'],p_levs,  '.-')
# #ax.plot(df['THTA'], df['HGHT'], '.-')
# ax.invert_yaxis()
# plt.show()







# # add to loop after
        
#         # add to all one df
#         df_all = df_all.append(df)
#         print('Adding data for ', date_i)
#         print(df_all.shape)
#     else: 
#         print(date_i,' sounding dataframe is empty... skipping this date/time.')
