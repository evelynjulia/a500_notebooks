#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Eve Wicksteed
#
# 11 December 2019


# test getting overlapping dates

from project.scripts.functions import get_full_date
from project.scripts.functions import get_overlap_dates
import pprint
# import get_full_date(the_file)

naefs_data_dir = "/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/"
naefs_files = "2016*/*SA.nc"

sonde_data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'
sonde_files = "*.csv"

dates_to_use = get_overlap_dates(naefs_dir= naefs_data_dir, naefs_files= naefs_files, sonde_dir = sonde_data_dir, sonde_files = sonde_files)


pprint.pprint(sorted(dates_to_use))
print(len(dates_to_use))


# test function to get sondes and plot 

import glob
from project.scripts.sondes.function_to_get_sondes import get_sonde_stabilty

data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'
fig_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/figures/'

list_of_files = sorted(glob.glob('/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/*.csv'))

top_pres = 850
stability_limit = 0.005 # what the cutoff is K/mb

get_sonde_stabilty(data_dir, fig_dir, list_of_files, top_pres, stability_limit)


### Open a pickle file
import pickle

fn1 = 'df_of_all_sondes_interp.pkl'
fn2 = 'df_of_all_sondes_orig.pkl'

pkl_file = open(data_dir+fn1, 'rb') # open a file, where you stored the pickled data
interp_snds = pickle.load(pkl_file) # dump information to that file
pkl_file.close() # close the file

pkl_file = open(data_dir+fn2, 'rb') 
orig_snds = pickle.load(pkl_file) 
pkl_file.close() 


import pandas as pd

snds_sm_dates = pd.DataFrame() # data frame of dates that over lap with naefs data

for i in range(len(interp_snds)):
    if int(interp_snds['COMP_DATE'].iloc[i]) in dates_to_use:
        print(i)
        print('yes')
        print(interp_snds['COMP_DATE'].iloc[i])
        # if the date is in, add line to new dataframe
        snds_sm_dates = snds_sm_dates.append(interp_snds.iloc[i])
    else:
        pass

# now I have a dataframe with all the same dates as in the naefs files


snds_sm_dates.mean(('COMP_DATE'))

# get the mean grouping by date and then pressure?
pd.groupby(snds_sm_dates,'COMP_DATE') #???

# then get naefs as well

