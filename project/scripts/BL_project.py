#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Eve Wicksteed
#
# 11 December 2019





# %% Imports
from project.scripts.functions import get_full_date
from project.scripts.functions import get_overlap_dates
import pprint
import glob
from project.scripts.sondes.function_to_get_sondes import get_sonde_stabilty
import pickle
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import pandas as pd


# %% Set directories 

data_dir = '/Users/ewicksteed/Documents/Eve/a500_notebooks_git_proj_version/project/data/'
fig_dir = '/Users/ewicksteed/Documents/Eve/a500_notebooks_git_proj_version/project/figures'

# %% Set constants

top_pres = 850
stability_limit = 0.067 # what the cutoff is K/mb

p0 = 100 #kPa
Rd=287.  #J/kg/K
cpd=1004.  #J/kg/K


# %% Read in some data
# 
# Dates to use
dates_pkl_file = open(data_dir+'dates_to_use.pkl', 'rb') 
dates_to_use = pickle.load(dates_pkl_file) 
dates_pkl_file.close() 


# Sondes data
pkl_file = open(data_dir+'df_of_all_sondes_interp.pkl', 'rb') # open a file, where you stored the pickled data
interp_snds = pickle.load(pkl_file) # dump information to that file
pkl_file.close() # close the file

pkl_file = open(data_dir+'df_of_all_sondes_orig.pkl', 'rb') 
orig_snds = pickle.load(pkl_file) 
pkl_file.close() 

# NAEFS data

pkl_file = open(data_dir+'all_naefs_df.pkl', 'rb') 
naefs_data = pickle.load(pkl_file) 
pkl_file.close() 



# %% Sondes
# 
# Limit the sondes to those with same dates and correct pressures
# now I have a dataframe with all the same dates as in the naefs files

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

# sonde data to use where the pressure values are only for 850, 925 and 1000
sonde_data_tu = snds_sm_dates[snds_sm_dates['PRES']>=850]


# get data in the right format
sonde_new = pd.DataFrame()
sonde_new['COMP_DATE'] = sonde_data_tu['COMP_DATE']
sonde_new['GRAD'] = sonde_data_tu['THTA_GRAD_INTERP']
sonde_new['PRES'] = sonde_data_tu['PRES']
sonde_new['THTA'] = sonde_data_tu['THTA']
sonde_new = sonde_new.reset_index(drop=True)

sonde_table = sonde_new.pivot(index = 'COMP_DATE', columns= 'PRES', values='THTA')
#grad = ((sonde_table.iloc[:,2] - sonde_table.iloc[:,1])/75 ) + ( (sonde_table.iloc[:,1] - sonde_table.iloc[:,0])/75 )
grad = ((sonde_table.iloc[:,1] - sonde_table.iloc[:,2])/75 )
sonde_table['1000'] = grad
sonde_table['925'] = grad
sonde_table['850'] = grad
sonde_table = sonde_table.reset_index()

sonde_table_back = pd.melt(sonde_table, id_vars=['COMP_DATE'], value_vars=['1000', '925', '850',])
# sort
sonde_table_back = sonde_table_back.sort_values(by=['COMP_DATE', 'PRES'])
sonde_table_back = sonde_table_back.reset_index(drop=True)

sonde_new['AV_GRAD'] = sonde_table_back['value']


# %% Calculate stability and TOD for sondes

stability_conditions = [
    sonde_new['AV_GRAD'] >= stability_limit,
    (sonde_new['AV_GRAD'] < stability_limit) & (sonde_new['AV_GRAD'] > -stability_limit),
    sonde_new['AV_GRAD'] <= -stability_limit ]

stability_choices = ['unstable', 'neutral', 'stable']  #['unstable', 'neutral', 'stable']
sonde_new['STABILITY'] = np.select(stability_conditions, stability_choices)

### GET TIME OF DAY COLUMN
sonde_new['TOD'] = sonde_new['COMP_DATE'].str[-2:]


# %% NAEFS


naefs_df_tu =  pd.DataFrame()
naefs_df_tu['COMP_DATE'] = naefs_data['COMP_DATE'] 
naefs_df_tu['TMP1000'] = naefs_data['TMP1000']
naefs_df_tu['TMP925'] = naefs_data['TMP925']
naefs_df_tu['TMP850'] = naefs_data['TMP850']

# calculate potential temperature
naefs_df_tu['THTA1000'] = naefs_df_tu['TMP1000']*((p0/100)**(Rd/cpd))
naefs_df_tu['THTA925'] = naefs_df_tu['TMP925']*((p0/92.5)**(Rd/cpd))
naefs_df_tu['THTA850'] = naefs_df_tu['TMP850']*((p0/85)**(Rd/cpd))

# calculate the average gradient below 850 
# used to identify stability
#naefs_df_tu['AV_GRAD'] = (naefs_df_tu['THTA1000'] - naefs_df_tu['THTA850'])/150
#naefs_df_tu['AV_GRAD'] = ((naefs_df_tu['THTA1000'] - naefs_df_tu['THTA925'])/75 ) + ( (naefs_df_tu['THTA925'] - naefs_df_tu['THTA850'])/75 )
naefs_df_tu['AV_GRAD'] = ((naefs_df_tu['THTA925'] - naefs_df_tu['THTA1000'])/75 ) 


# get data in the right format
p1df = pd.DataFrame()
p1df['COMP_DATE'] = naefs_df_tu['COMP_DATE']
p1df['AV_GRAD'] = naefs_df_tu['AV_GRAD']
p1df['PRES'] = 1000.0
p1df['THTA'] = naefs_df_tu['THTA1000']

p2df = pd.DataFrame()
p2df['COMP_DATE'] = naefs_df_tu['COMP_DATE']
p2df['AV_GRAD'] = naefs_df_tu['AV_GRAD']
p2df['PRES'] = 925.0
p2df['THTA'] = naefs_df_tu['THTA925']

p3df = pd.DataFrame()
p3df['COMP_DATE'] = naefs_df_tu['COMP_DATE']
p3df['AV_GRAD'] = naefs_df_tu['AV_GRAD']
p3df['PRES'] = 850.0
p3df['THTA'] = naefs_df_tu['THTA850']

new_naefs_df_tu = pd.concat([p1df,p2df,p3df])

# then sort by date and pressure
new_naefs_df_tu.sort_values(by=['COMP_DATE', 'PRES'])


# %% Calculate stability and TOD for NAEFS

stability_conditions = [
    new_naefs_df_tu['AV_GRAD'] >= stability_limit,
    (new_naefs_df_tu['AV_GRAD'] < stability_limit) & (new_naefs_df_tu['AV_GRAD'] > -stability_limit),
    new_naefs_df_tu['AV_GRAD'] <= -stability_limit ]

stability_choices = ['unstable', 'neutral', 'stable']  #['unstable', 'neutral', 'stable']
new_naefs_df_tu['STABILITY'] = np.select(stability_conditions, stability_choices)

### GET TIME OF DAY COLUMN
new_naefs_df_tu['TOD'] = new_naefs_df_tu['COMP_DATE'].str[-2:]


# %% same format dfs for naefs and sondes

sondes = pd.DataFrame()
sondes['COMP_DATE'] = sonde_new['COMP_DATE']
sondes['AV_GRAD'] = sonde_new['AV_GRAD']
sondes['PRES'] = sonde_new['PRES']
sondes['THTA'] = sonde_new['THTA']
sondes['STABILITY'] = sonde_new['STABILITY']
sondes['TOD'] = sonde_new['TOD']
# sort
sondes = sondes.sort_values(by=['COMP_DATE', 'PRES'])
# reset indices
sondes = sondes.reset_index(drop=True)

naefs = pd.DataFrame()
naefs['COMP_DATE'] = new_naefs_df_tu['COMP_DATE']
naefs['AV_GRAD'] = new_naefs_df_tu['AV_GRAD']
naefs['PRES'] = new_naefs_df_tu['PRES']
naefs['THTA'] = new_naefs_df_tu['THTA']
naefs['STABILITY'] = new_naefs_df_tu['STABILITY']
naefs['TOD'] = new_naefs_df_tu['TOD']
# sort
naefs = naefs.sort_values(by=['COMP_DATE', 'PRES'])
# reset indices
naefs = naefs.reset_index(drop=True)


# %% Check dataframes are the same

test = (sondes['COMP_DATE'].astype(float) - naefs['COMP_DATE'].astype(float))[:]
for ind, line in enumerate(test):
    print(ind, line)


naefs = naefs.drop([192, 193, 194])

sondes = sondes.reset_index(drop=True)
naefs= naefs.reset_index(drop=True)


# and then can check they're the same by 
test = (sondes['COMP_DATE'].astype(float) - naefs['COMP_DATE'].astype(float))[:]
sum(test) # if this gives me 0 then my dataframes are the same and I can compare my naefs data to my sonde data


# %% Plot histograms of stability

sondes_stability_keys = np.array(sondes.groupby('COMP_DATE').first().groupby('STABILITY').count()['TOD'].keys())
sondes_stability_vals = sondes.groupby('COMP_DATE').first().groupby('STABILITY').count()['TOD'].values

naefs_stability_keys = np.array(naefs.groupby('COMP_DATE').first().groupby('STABILITY').count()['TOD'].keys())
naefs_stability_vals = naefs.groupby('COMP_DATE').first().groupby('STABILITY').count()['TOD'].values

fig, ax = plt.subplots(1,2, figsize=(15,9))
ax[0].bar(sondes_stability_keys, sondes_stability_vals)
ax[0].set_ylabel('Count')
ax[0].set_xlabel('Stability class')
ax[0].set_title('SONDES')
ax[1].bar(naefs_stability_keys, naefs_stability_vals)
ax[1].set_ylabel('Count')
ax[1].set_xlabel('Stability class')
ax[1].set_title('NAEFS')
ax[0].set_ylim(0,70)
ax[1].set_ylim(0,70)
plt.show()
#plt.savefig(fig_dir+'bar_stab_classes_and_grad'+run_date+'run_stablim'+str(stability_limit)+'.png')



