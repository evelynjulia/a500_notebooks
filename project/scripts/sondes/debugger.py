# reproducibe example
# eve
# 3 december

import pickle

import glob
import numpy as np
import datetime as dt
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import interpolate

# pickle file

# data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'
# debug_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/debug/'
# list_of_files = glob.glob('/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/*.csv')
# len_date = 10

# for file in list_of_files[0:4]:
#     df = pd.read_csv(file, index_col= 'Unnamed: 0')
#     date_i = os.path.basename(file)[0:len_date]
#     pkl_file = open(debug_dir+date_i+'.pkl', 'wb')
#     pickle.dump(df, pkl_file)
#     pkl_file.close()





# OPEN THE DATA


debug_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/debug/'
len_date = 10

list_of_files = glob.glob(debug_dir+'*.pkl')
p_levs = [1000, 925, 850, 700, 500, 250, 200]

for file in list_of_files:
    print(file)
    pkl_file = open(file, 'rb') # open a file, where you stored the pickled data
    df = pickle.load(pkl_file) # dump information to that file
    pkl_file.close() # close the file
    #print(df)
    date_i = os.path.basename(file)[0:len_date]
    print(date_i)
    hr_i = date_i[-2:]
    print(hr_i)
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
        stability_conditions = [
            new_df_i['THTA_GRAD'][0] >= 0.005,
            (new_df_i['THTA_GRAD'][0] < 0.005) & (new_df_i['THTA_GRAD'][0] > -0.05),
            new_df_i['THTA_GRAD'][0] <= -0.005]
        stability_choices = [1, 0, -1]  #['stable', 'neutral', 'unstable']
        new_df_i['STABILITY'] = np.select(stability_conditions, stability_choices)

        # column for day / night (Time Of Day)
        tod_conditions = [
            hr_i == '00',
            hr_i == '12']
        tod_choices = [0, 12]  #['night', 'day']
        new_df_i['TOD'] = np.select(tod_conditions, tod_choices)
        
        print(new_df_i)
    else: 
        print(date_i,' sounding dataframe is empty... skipping this date/time.')

