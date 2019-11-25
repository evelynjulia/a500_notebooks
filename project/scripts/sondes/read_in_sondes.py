# Eve Wicksteed
#
# 23 November 2019

import glob
from netCDF4 import Dataset
import numpy as np
import datetime as dt
from a500.utils import ncdump
from netCDF4 import num2date, date2num
import pandas as pd
import os

import pickle


data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'

list_of_files = glob.glob('/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/*.csv')

len_date = 10

# read all into one dataframe and then groupby date

df_all = pd.DataFrame()
for file in list_of_files[0:3]:
    df = pd.read_csv(file, index_col= 'Unnamed: 0')
    date_i = os.path.basename(file)[0:len_date]
    if df.shape[0] > 0:
        df_all = df_all.append(df)
        print('Adding data for ', date_i)
        print(df_all.shape)
    else: 
        print(date_i,' sounding dataframe is empty... skipping this date/time.')

# what about multi index? for date and then height / pressure
## not sure this multi index thing will work
# df_all.set_index('DATE')
# df_all.set_index(['DATE', 'HGHT'], inplace=True)
# df_all.set_index(['HGHT', 'DATE'], inplace=True)
# df_all.groupby(level=1).mean()

df.set_index('HGHT', inplace=True)
df.groupby('DATE')['THTV'].plot(legend=True)




# To read in data and combine all into a df with date as columns and height/ theta v as rows
# For theta-V ('THTV' in the sondes)
# get date
date, theta_v, hgts = [], [], []
for file in list_of_files[0:4]:
    #print(file)
    #print(os.path.basename(file))
    date_i = os.path.basename(file)[0:len_date]
    print(date_i)
    df = pd.read_csv(file)
    if df.shape[0] > 0:
        t_v_i = np.array(df['THTV'][0:20])
        hgts_i = np.array(df['HGHT'][0:20])
        theta_v.append(t_v_i)
        date.append(date_i)
        hgts.append(hgts_i)
    else: 
        print('Sounding dataframe is empty... skipping this date/time:', date_i)


all_tv = np.stack(theta_v)
all_hgts = np.stack(hgts)
# the above corresponds to the following date order
all_dates = np.stack(date)


sonde_df_tv = pd.DataFrame(all_tv.T, columns = all_dates)
sonde_df_height = pd.DataFrame(all_hgts.T, columns = all_dates)
    
