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
    

#pd.read_csv("/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/2016082712_sounding_68816.csv")


#stn_no = os.path.basename(list_of_files[0])[20:25]
#date = os.path.basename(list_of_files[0])[0:len_date]

# do this for theta_v ('THTV')

date = []
for file in list_of_files:
    
    # print date
    print(os.path.basename(file)) # get the actual file name
    eves_file = Dataset(file,'r') 
    #print(eves_file.variables.keys())
    

    #hgt85_i = np.array(eves_file.variables['HGT_850mb'][0,...])
    hgt85_i = np.array(eves_file.variables['HGT_850mb'][0,...]).flatten() # to get a flat array

    

    
    # get the date
    #date_of_run = num2date(time,units=time_units)[0]
    #date_i = dt.datetime.strftime(date_of_run,"%Y%m%d%H")
    date_i = os.path.basename(file)[0:len_date]
    print(date_i)

    #hgt85.append(hgt85_i)
    date.append(date_i)


all_hgt85 = np.stack(hgt85)

# the above corresponds to the following date order
all_dates = np.stack(date)