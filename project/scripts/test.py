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

import glob
from project.scripts.sondes.function_to_get_sondes import get_sonde_stabilty

import pickle

import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

import pandas as pd


naefs_data_dir = "/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/"
naefs_files = "2016*/*SA.nc"

sonde_data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'
sonde_files = "*.csv"

dates_to_use = get_overlap_dates(naefs_dir= naefs_data_dir, naefs_files= naefs_files, sonde_dir = sonde_data_dir, sonde_files = sonde_files)


pprint.pprint(sorted(dates_to_use))
print(len(dates_to_use))


# test function to get sondes and plot 


data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'
fig_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/figures/'

list_of_files = sorted(glob.glob('/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/*.csv'))

top_pres = 850
stability_limit = 0.005 # what the cutoff is K/mb

get_sonde_stabilty(data_dir, fig_dir, list_of_files, top_pres, stability_limit)


### Open a pickle file


fn1 = 'df_of_all_sondes_interp.pkl'
fn2 = 'df_of_all_sondes_orig.pkl'

pkl_file = open(data_dir+fn1, 'rb') # open a file, where you stored the pickled data
interp_snds = pickle.load(pkl_file) # dump information to that file
pkl_file.close() # close the file

pkl_file = open(data_dir+fn2, 'rb') 
orig_snds = pickle.load(pkl_file) 
pkl_file.close() 




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


#snds_sm_dates.mean(('COMP_DATE'))

# get the mean grouping by date and then pressure?
#grouped = snds_sm_dates.groupby('COMP_DATE') #???
#grouped.first() # prints the first of each column





keys = np.array(snds_sm_dates.groupby('COMP_DATE').first().groupby('STABILITY').count()['DATE'].keys())
vals = snds_sm_dates.groupby('COMP_DATE').first().groupby('STABILITY').count()['DATE'].values


run_date = dt.datetime.now().strftime('%y%m%d')

fig, ax = plt.subplots(1,2, figsize=(15,9))
ax[0].bar(keys, vals)
ax[0].set_ylabel('Count')
ax[0].set_xlabel('Stability class')
ax[1].hist(snds_sm_dates.groupby('COMP_DATE').first()['MEAN_GRAD_BELOW_850'],50)
ax[1].set_xlabel('Mean gradient between 1000mb and 850mb')
#plt.title('Number of cases in each stability class')
plt.savefig(fig_dir+'bar_stab_classes_and_grad'+run_date+'run_stablim'+str(stability_limit)+'.png')


#### 
# now plot sondes for the right data

# get means for different classes


# grouped by stability class
gbs =  snds_sm_dates.groupby('STABILITY') 
gbs.groups.keys()

# sonde data to use where the pressure values are only for 850, 925 and 1000
sonde_data_tu = snds_sm_dates[snds_sm_dates['PRES']>=850]

# get some averages
day_lev_av = sonde_data_tu.groupby(['STABILITY','PRES','COMP_DATE'])['THTA'].mean()

# averages over all dates
stab_lev_av = sonde_data_tu.groupby(['STABILITY','PRES'])['THTA'].mean()
stab_lev_TOD_av = sonde_data_tu.groupby(['STABILITY','PRES','TOD'])['THTA'].mean()

lev_TOD_av = sonde_data_tu.groupby(['PRES','TOD'])['THTA'].mean()

stab = ['Neutral', 'Stable', 'Unstable']
Pres = [850,925, 1000]
tod = ['00', '12']

fig, ax = plt.subplots(1,1, figsize=(15,9))
ax.plot(stab_lev_av.unstack().iloc[0], Pres)
ax.plot(stab_lev_av.unstack().iloc[1], Pres)
ax.plot(stab_lev_av.unstack().iloc[2], Pres)
ax.set_ylabel('Pressure')
ax.set_xlabel('Theta')
ax.invert_yaxis()
plt.legend(stab)
plt.title('Mean theta by stability class')
plt.savefig(fig_dir+'mean_stab_class_sonde'+run_date+'run_stablim'+str(stability_limit)+'.png')



fig, ax = plt.subplots(1,1, figsize=(15,9))
ax.plot(lev_TOD_av.unstack().T.iloc[0], Pres)
ax.plot(lev_TOD_av.unstack().T.iloc[1], Pres)
ax.set_ylabel('Pressure')
ax.set_xlabel('Theta')
ax.invert_yaxis()
plt.legend(tod)
plt.title('Mean theta by time of sounding')
plt.savefig(fig_dir+'mean_TOD_sonde'+run_date+'run_stablim'+str(stability_limit)+'.png')






# then get naefs as well

pkl_file = open(naefs_data_dir+'all_naefs_df.pkl', 'rb') 
naefs_data = pickle.load(pkl_file) 
pkl_file.close() 


# make potential temp in df
p0=1.e5
Rd=287.  #J/kg/K
cpd=1004.  #J/kg/K
#CT_theta=CT_temp.variables.values*(p0/CT_press**(Rd/cpd))


naefs_df_tu =  pd.DataFrame()
naefs_df_tu['COMP_DATE'] = naefs_data['COMP_DATE'] 
naefs_df_tu['TMP1000'] = naefs_data['TMP1000']
naefs_df_tu['TMP925'] = naefs_data['TMP925']
naefs_df_tu['TMP850'] = naefs_data['TMP850']

naefs_df_tu['THTA1000'] = naefs_df_tu['TMP1000']*((p0/100000)**(Rd/cpd))
naefs_df_tu['THTA925'] = naefs_df_tu['TMP925']*((p0/100000)**(Rd/cpd))
naefs_df_tu['THTA850'] = naefs_df_tu['TMP850']*((p0/100000)**(Rd/cpd))

naefs_df_tu['AV_GRAD'] = (naefs_df_tu['THTA1000'] - naefs_df_tu['THTA850'])/150


naefs_day_means = naefs_df_tu.groupby(['COMP_DATE']).mean()
all_neafs_means = naefs_day_means.mean()

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

new_naefs_df_tu.sort_values(by=['COMP_DATE', 'PRES'])



############ CALCULATE STABILITY FOR NAEFS DATA

stability_conditions = [
    new_naefs_df_tu['AV_GRAD'] >= stability_limit,
    (new_naefs_df_tu['AV_GRAD'] < stability_limit) & (new_naefs_df_tu['AV_GRAD'] > -stability_limit),
    new_naefs_df_tu['AV_GRAD'] <= -stability_limit ]

stability_choices = ['unstable', 'neutral', 'stable']  #['unstable', 'neutral', 'stable']
new_naefs_df_tu['STABILITY'] = np.select(stability_conditions, stability_choices)

### GET TIME OF DAY COLUMN
new_naefs_df_tu['TOD'] = new_naefs_df_tu['COMP_DATE'].str[-2:]

new_naefs_df_tu