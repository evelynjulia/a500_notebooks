#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Eve Wicksteed
#
# 11 December 2019




# test getting overlapping dates
# %%
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

# %%
naefs_data_dir = "/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/"
naefs_files = "2016*/*SA.nc"

sonde_data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'
sonde_files = "*.csv"

dates_to_use = get_overlap_dates(naefs_dir= naefs_data_dir, naefs_files= naefs_files, sonde_dir = sonde_data_dir, sonde_files = sonde_files)


# pprint.pprint(sorted(dates_to_use))
# print(len(dates_to_use))


# test function to get sondes and plot 


data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'
fig_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/figures/'

list_of_files = sorted(glob.glob('/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/*.csv'))

top_pres = 850
#stability_limit = 0.005 # what the cutoff is K/mb
stability_limit = 0.067 # what the cutoff is K/mb

# %%
get_sonde_stabilty(data_dir, fig_dir, list_of_files, top_pres, stability_limit)


### Open a pickle file
# read in sonds data

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


#######################################################################
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




###################################################################
# NAEFS

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

#naefs_df_tu['AV_GRAD'] = (naefs_df_tu['THTA1000'] - naefs_df_tu['THTA850'])/150
naefs_df_tu['AV_GRAD'] = ((naefs_df_tu['THTA1000'] - naefs_df_tu['THTA925'])/75 ) + ( (naefs_df_tu['THTA925'] - naefs_df_tu['THTA850'])/75 )


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



###################################################################
# now make the sonde df exactly the same as the naefs one:
df1_s = pd.DataFrame()
df1_s['COMP_DATE'] = sonde_data_tu['COMP_DATE']
df1_s['AV_GRAD'] = sonde_data_tu['THTA_GRAD_INTERP']
df1_s['PRES'] = sonde_data_tu['PRES']
df1_s['THTA'] = sonde_data_tu['THTA']
df1_s['STABILITY'] = sonde_data_tu['STABILITY']
df1_s['TOD'] = sonde_data_tu['TOD']

df2_n = new_naefs_df_tu.copy()
df2_n['THTA'] = df2_n['THTA'].round()

df1_s
df2_n

# sort by date and then pressure so that they're in the same order... 
df1_s = df1_s.sort_values(by=['COMP_DATE', 'PRES'])
df2_n = df2_n.sort_values(by=['COMP_DATE', 'PRES'])

df1_s = df1_s.reset_index(drop=True)
df2_n = df2_n.reset_index(drop=True)

#####################################################
# check that the dataframes are the same

# and then can check they're the same by 
test = (df1_s['COMP_DATE'].astype(float) - df2_n['COMP_DATE'].astype(float))[:]

for ind, line in enumerate(test):
    print(ind, line)


# sondes data is missing 2016083100
# easy fix is to remove that date from naefs
### 192 
# np.where(df2_n['COMP_DATE']==str(2016081300)))
# df1_s['COMP_DATE'][190:200]

# df2_n['COMP_DATE'][190:200]




#### so the sonds df (df1_s) is the right size maybe?

df2_n = df2_n.drop([192, 193, 194])


df1_s = df1_s.reset_index(drop=True)
df2_n = df2_n.reset_index(drop=True)


df1_s
df2_n


# and then can check they're the same by 
test = (df1_s['COMP_DATE'].astype(float) - df2_n['COMP_DATE'].astype(float))[:]
sum(test) # if this gives me 0 then my dataframes are the same and I can compare my naefs data to my sonde data



###########################################################
# plot comparisons of average theta

sonde_stability_level_av_thta = df1_s.groupby(['STABILITY','PRES'])['THTA'].mean()
#sonde_stability_level_TOD_av_thta = df1_s.groupby(['STABILITY','PRES','TOD'])['THTA'].mean()
naefs_stability_level_av_thta = df2_n.groupby(['STABILITY','PRES'])['THTA'].mean()
#naefs_stability_level_TOD_av_thta = df2_n.groupby(['STABILITY','PRES','TOD'])['THTA'].mean()

sonde_lev_TOD_av = df1_s.groupby(['PRES','TOD'])['THTA'].mean()
naefs_lev_TOD_av = df2_n.groupby(['PRES','TOD'])['THTA'].mean()

stab = ['Stable', 'Unstable', 'Neutral']
Pres = [850,925, 1000]
tod = ['00', '12']

fig, ax = plt.subplots(2,1, figsize=(15,9))
#plt.title('Mean theta by stability class')
ax[0].plot(sonde_stability_level_av_thta.unstack().iloc[0], Pres)
ax[0].plot(sonde_stability_level_av_thta.unstack().iloc[1], Pres)
ax[0].plot(sonde_stability_level_av_thta.unstack().iloc[2], Pres)
ax[1].plot(naefs_stability_level_av_thta.unstack().iloc[0], Pres)
ax[1].plot(naefs_stability_level_av_thta.unstack().iloc[1], Pres)
ax[1].plot(naefs_stability_level_av_thta.unstack().iloc[2], Pres)
ax[0].set_title('SONDES')
ax[1].set_title('NAEFS')
ax[0].set_xlim(280,300)
ax[1].set_xlim(280,300)
ax[0].set_ylabel('Pressure')
#ax[0].set_xlabel('Theta')
ax[1].set_ylabel('Pressure')
ax[1].set_xlabel('Theta')
ax[0].invert_yaxis()
ax[1].invert_yaxis()
plt.legend(stab)
#plt.show()
plt.savefig(fig_dir+'Comparison_average_theta_by_stab_class'+run_date+'run_stablim'+str(stability_limit)+'.png')



fig, ax = plt.subplots(2,1, figsize=(15,9))
ax[0].plot(sonde_lev_TOD_av.unstack().T.iloc[0], Pres)
ax[0].plot(sonde_lev_TOD_av.unstack().T.iloc[1], Pres)
ax[1].plot(naefs_lev_TOD_av.unstack().T.iloc[0], Pres)
ax[1].plot(naefs_lev_TOD_av.unstack().T.iloc[1], Pres)
ax[0].set_title('SONDES')
ax[1].set_title('NAEFS')
ax[0].set_ylabel('Pressure')
ax[0].set_xlim(280,300)
ax[1].set_xlim(280,300)
#ax[0].set_xlabel('Theta')
ax[0].invert_yaxis()
ax[1].invert_yaxis()
ax[1].set_ylabel('Pressure')
ax[1].set_xlabel('Theta')
plt.legend(tod)
#plt.title('Mean theta by time of sounding')
#plt.show()
plt.savefig(fig_dir+'Comparison_average_theta_by_TOD'+run_date+'run_stablim'+str(stability_limit)+'.png')



#####################################################

df1_s
df2_n

# model error:

# MAE: 
MAE_thta_all_levs = sum( np.abs(df1_s['THTA'] - df2_n['THTA']) ) / (len(df1_s['THTA']))
MAE_thta_1000 = sum( np.abs(df1_s['THTA'][df1_s['PRES']==1000] - df2_n['THTA'][df1_s['PRES']==1000]) ) / (len(df1_s['THTA'][df1_s['PRES']==1000]))
MAE_thta_925 = sum( np.abs(df1_s['THTA'][df1_s['PRES']==925] - df2_n['THTA'][df1_s['PRES']==925]) ) / (len(df1_s['THTA'][df1_s['PRES']==925]))
MAE_thta_850 = sum( np.abs(df1_s['THTA'][df1_s['PRES']==850] - df2_n['THTA'][df1_s['PRES']==850]) ) / (len(df1_s['THTA'][df1_s['PRES']==850]))

# 6.5473684210526315 (degrees C) all levels
# 1000 = 1.3894736842105264
#  925 = 5.7368421052631575
# 850 = 12.51578947368421

MAPE_thta_all_levs = ( sum( np.abs( (df1_s['THTA'] - df2_n['THTA']) / df1_s['THTA'] ) ) / (len(df1_s['THTA'])) )*100
MAPE_thta_1000 = ( sum( np.abs( (df1_s['THTA'][df1_s['PRES']==1000] - df2_n['THTA'][df1_s['PRES']==1000]) / df1_s['THTA'][df1_s['PRES']==1000] ) ) / (len(df1_s['THTA'][df1_s['PRES']==1000])) )*100
MAPE_thta_925 = ( sum( np.abs( (df1_s['THTA'][df1_s['PRES']==925] - df2_n['THTA'][df1_s['PRES']==925]) / df1_s['THTA'][df1_s['PRES']==925] ) ) / (len(df1_s['THTA'][df1_s['PRES']==925])) )*100
MAPE_thta_850 = ( sum( np.abs( (df1_s['THTA'][df1_s['PRES']==850] - df2_n['THTA'][df1_s['PRES']==850]) / df1_s['THTA'][df1_s['PRES']==850] ) ) / (len(df1_s['THTA'][df1_s['PRES']==850])) )*100

### MAPE (%)
# all levs: 2.226939155093236
# 1000 = 0.48386672774818307
# 925 = 1.9622621853483255
# 850 = 4.234688552183197


#####################################################
# MORE PLOTS --> histograms

df1_stability_keys = np.array(df1_s.groupby('COMP_DATE').first().groupby('STABILITY').count()['TOD'].keys())
df1_stability_vals = df1_s.groupby('COMP_DATE').first().groupby('STABILITY').count()['TOD'].values

df2_stability_keys = np.array(df2_n.groupby('COMP_DATE').first().groupby('STABILITY').count()['TOD'].keys())
df2_stability_vals = df2_n.groupby('COMP_DATE').first().groupby('STABILITY').count()['TOD'].values



fig, ax = plt.subplots(1,2, figsize=(15,9))
ax[0].bar(df1_stability_keys, df1_stability_vals)
ax[0].set_ylabel('Count')
ax[0].set_xlabel('Stability class')
ax[1].bar(df2_stability_keys, df2_stability_vals)
ax[1].set_ylabel('Count')
ax[1].set_xlabel('Stability class')
#ax[1].hist(snds_sm_dates.groupby('COMP_DATE').first()['MEAN_GRAD_BELOW_850'],50)
#ax[1].set_xlabel('Mean gradient between 1000mb and 850mb')
#plt.title('Number of cases in each stability class')
plt.show()
plt.savefig(fig_dir+'bar_stab_classes_and_grad'+run_date+'run_stablim'+str(stability_limit)+'.png')








#### trying to recalculate the sonde gradients (the same way I calculated the naefs ones)

ptable = (df1_s.pivot(index = 'COMP_DATE', columns= 'PRES', values='THTA'))
test2 = (ptable[1000]-ptable[850])/150
plt.hist(test2)
plt.show()
#naefs_df_tu['AV_GRAD'] = (naefs_df_tu['THTA1000'] - naefs_df_tu['THTA850'])/150




