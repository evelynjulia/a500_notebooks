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
fig_dir = '/Users/ewicksteed/Documents/Eve/a500_notebooks_git_proj_version/project/figures/new_to_use/'

# %% Set constants

top_pres = 850
stability_limit = 0.02 # what the cutoff is K/mb

p0 = 100 #kPa
Rd=287.  #J/kg/K
cpd=1004.  #J/kg/K

run_date = dt.datetime.now().strftime('%y%m%d')

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
sonde_new['HGHT'] = sonde_data_tu['HGHT']
sonde_new = sonde_new.reset_index(drop=True)

sonde_table = sonde_new.pivot(index = 'COMP_DATE', columns= 'PRES', values='THTA')
# calculate the temp difference in the bottom layer
diff = ((sonde_table.iloc[:,1] - sonde_table.iloc[:,2])/75 ) # 925 - 1000

sonde_table['1000'] = diff
sonde_table['925'] = diff
sonde_table['850'] = diff
sonde_table = sonde_table.reset_index()

sonde_table_back = pd.melt(sonde_table, id_vars=['COMP_DATE'], value_vars=['1000', '925', '850',])
# sort
sonde_table_back = sonde_table_back.sort_values(by=['COMP_DATE', 'PRES'])
sonde_table_back = sonde_table_back.reset_index(drop=True)

sonde_new['DIFF'] = sonde_table_back['value']


# %% Calculate stability and TOD for sondes

stability_conditions = [
    sonde_new['DIFF'] >= stability_limit,
    (sonde_new['DIFF'] < stability_limit) & (sonde_new['DIFF'] > -stability_limit),
    sonde_new['DIFF'] <= -stability_limit ]

stability_choices = ['stable', 'neutral', 'unstable']  #['unstable', 'neutral', 'stable']
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
naefs_df_tu['DIFF'] = ((naefs_df_tu['THTA925'] - naefs_df_tu['THTA1000'])/75 ) 
#diff = ((sonde_table.iloc[:,1] - sonde_table.iloc[:,2])/75 ) # 925 - 1000

# get data in the right format
p1df = pd.DataFrame()
p1df['COMP_DATE'] = naefs_df_tu['COMP_DATE']
p1df['DIFF'] = naefs_df_tu['DIFF']
p1df['PRES'] = 1000.0
p1df['THTA'] = naefs_df_tu['THTA1000']

p2df = pd.DataFrame()
p2df['COMP_DATE'] = naefs_df_tu['COMP_DATE']
p2df['DIFF'] = naefs_df_tu['DIFF']
p2df['PRES'] = 925.0
p2df['THTA'] = naefs_df_tu['THTA925']

p3df = pd.DataFrame()
p3df['COMP_DATE'] = naefs_df_tu['COMP_DATE']
p3df['DIFF'] = naefs_df_tu['DIFF']
p3df['PRES'] = 850.0
p3df['THTA'] = naefs_df_tu['THTA850']

new_naefs_df_tu = pd.concat([p1df,p2df,p3df])

# then sort by date and pressure
new_naefs_df_tu = new_naefs_df_tu.sort_values(by=['COMP_DATE', 'PRES'])


# %% Calculate stability and TOD for NAEFS

stability_conditions = [
    new_naefs_df_tu['DIFF'] >= stability_limit,
    (new_naefs_df_tu['DIFF'] < stability_limit) & (new_naefs_df_tu['DIFF'] > -stability_limit),
    new_naefs_df_tu['DIFF'] <= -stability_limit ]

stability_choices = ['stable', 'neutral', 'unstable']  #['unstable', 'neutral', 'stable']
new_naefs_df_tu['STABILITY'] = np.select(stability_conditions, stability_choices)

### GET TIME OF DAY COLUMN
new_naefs_df_tu['TOD'] = new_naefs_df_tu['COMP_DATE'].str[-2:]


# %% same format dfs for naefs and sondes

sondes = pd.DataFrame()
sondes['COMP_DATE'] = sonde_new['COMP_DATE']
sondes['DIFF'] = sonde_new['DIFF']
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
naefs['DIFF'] = new_naefs_df_tu['DIFF']
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


# %% Bar plot of stability

sondes_stability_keys = np.array(sondes.groupby('COMP_DATE').first().groupby('STABILITY').count()['TOD'].keys())
sondes_stability_vals = sondes.groupby('COMP_DATE').first().groupby('STABILITY').count()['TOD'].values

naefs_stability_keys = np.array(naefs.groupby('COMP_DATE').first().groupby('STABILITY').count()['TOD'].keys())
naefs_stability_vals = naefs.groupby('COMP_DATE').first().groupby('STABILITY').count()['TOD'].values


fig, ax = plt.subplots(1,2, figsize=(15,9))
ax[0].bar(sondes_stability_keys, sondes_stability_vals, color = 'red')
ax[0].set_ylabel('Count')
ax[0].set_xlabel('Stability class')
ax[0].set_title('SONDES')
ax[1].bar(naefs_stability_keys, naefs_stability_vals, color = 'orange')
ax[1].set_ylabel('Count')
ax[1].set_xlabel('Stability class')
ax[1].set_title('NAEFS')
ax[0].set_ylim(0,80)
ax[1].set_ylim(0,80)
#plt.show()
plt.savefig(fig_dir+'Bar_plot'+run_date+'run_stablim'+str(stability_limit)+'.png')


# %% Bar plot of stabtime of day

sondes_tod_keys = np.array(sondes.groupby('COMP_DATE').first().groupby('TOD').count()['STABILITY'].keys())
sondes_tod_vals = sondes.groupby('COMP_DATE').first().groupby('TOD').count()['STABILITY'].values

naefs_tod_keys = np.array(naefs.groupby('COMP_DATE').first().groupby('TOD').count()['STABILITY'].keys())
naefs_tod_vals = naefs.groupby('COMP_DATE').first().groupby('TOD').count()['STABILITY'].values


fig, ax = plt.subplots(1,1, figsize=(15,9))
ax.bar(sondes_tod_keys, sondes_tod_vals)
#ax.bar(naefs_tod_keys, naefs_tod_vals, color = 'orange')
ax.set_ylabel('Count')
ax.set_xlabel('Time of day')
ax.set_title('Number of cases by time of day')
# ax.set_ylim(0,80)
#plt.show()
plt.savefig(fig_dir+'Bar_plot_tod_'+run_date+'run_stablim'+str(stability_limit)+'.png')



# %% Calculate averages

# mean by stability
sonde_stability_level_av_thta = sondes.groupby(['STABILITY','PRES'])['THTA'].mean()
naefs_stability_level_av_thta = naefs.groupby(['STABILITY','PRES'])['THTA'].mean()

# mean bu time of day
sonde_lev_TOD_av = sondes.groupby(['PRES','TOD'])['THTA'].mean()
naefs_lev_TOD_av = naefs.groupby(['PRES','TOD'])['THTA'].mean()

# %% Plots for comparison of av theta

Pres = [850,925, 1000]
tod = ['00', '12']
leg = ['Neutral', 'Stable'] #, 'Unstable'] 

# by stability class
fig, ax = plt.subplots(1,1, figsize=(15,9))
ax.plot(sonde_stability_level_av_thta.unstack().iloc[0], Pres, '-.', color='red')
ax.plot(sonde_stability_level_av_thta.unstack().iloc[1], Pres, color='red')
ax.plot(naefs_stability_level_av_thta.unstack().iloc[0], Pres, '-.', color='orange')
ax.plot(naefs_stability_level_av_thta.unstack().iloc[1], Pres, color='orange')
ax.set_ylabel('Pressure (kPa)')
ax.set_xlabel('Potential temperature (K)')
ax.invert_yaxis()
ax.legend(['Neutral - sonde', 'Stable - sonde', 'Neutral - NAEFS', 'Stable - NAEFS'])
ax.set_title('Average potential temperature profile by stability class')
#plt.show()
plt.savefig(fig_dir+'Comparison_average_theta_by_stab_class_all'+run_date+'run_stablim'+str(stability_limit)+'.png')



# by time of day
fig, ax = plt.subplots(1,1, figsize=(15,9))
ax.plot(sonde_lev_TOD_av.unstack().T.iloc[0], Pres, '-.', color='red')
ax.plot(sonde_lev_TOD_av.unstack().T.iloc[1], Pres, color='red')
ax.plot(naefs_lev_TOD_av.unstack().T.iloc[0], Pres, '-.', color='orange')
ax.plot(naefs_lev_TOD_av.unstack().T.iloc[1], Pres, color='orange')
ax.set_ylabel('Pressure (kPa)')
ax.set_xlabel('Potential temperature (K)')
ax.invert_yaxis()
ax.legend(['00 - sonde', '12 - sonde', '00 - NAEFS', '12 - NAEFS'])
ax.set_title('Average potential temperature profile by time of day')
#plt.show()
plt.savefig(fig_dir+'Comparison_average_theta_by_TOD_all'+run_date+'run_stablim'+str(stability_limit)+'.png')



# %% Plot sonde versus model data - potentential temp

pres = [850,925,1000]

# convert so easy to plot
ptable_sondes = (sondes.pivot(index = 'PRES', columns= 'COMP_DATE', values='THTA'))
ptable_naefs = (naefs.pivot(index = 'PRES', columns= 'COMP_DATE', values='THTA'))


fig, ax = plt.subplots(2,1, figsize=(15,9))
ax[0].plot(ptable_sondes, pres)
ax[1].plot(ptable_naefs, pres)
ax[0].set_title('SONDES')
ax[1].set_title('NAEFS')
ax[0].set_xlim(280,310)
ax[1].set_xlim(280,310)
ax[0].set_ylabel('Pressure (kPa)')
#ax[0].set_xlabel('Potential Temperature (K)')
ax[1].set_ylabel('Pressure (kPa)')
ax[1].set_xlabel('Potential Temperature (K)')
ax[0].invert_yaxis()
ax[1].invert_yaxis()
#plt.show()
plt.savefig(fig_dir+'actual_data_model_v_obs'+run_date+'.png')


# %% calculate error:

# set constants:
snd1000 = sondes['THTA'][sondes['PRES']==1000]
snd925 = sondes['THTA'][sondes['PRES']==925]
snd850 = sondes['THTA'][sondes['PRES']==850]
nfs1000 = naefs['THTA'][sondes['PRES']==1000]
nfs925 = naefs['THTA'][sondes['PRES']==925]
nfs850 = naefs['THTA'][sondes['PRES']==850]


# MAE: 
MAE_thta_all_levs = sum( np.abs(sondes['THTA'] - naefs['THTA']) ) / (len(sondes['THTA']))
MAE_thta_1000 = sum( np.abs(snd1000 - nfs1000) ) / (len(snd1000))
MAE_thta_925 = sum( np.abs(snd925 - nfs925) ) / (len(snd925))
MAE_thta_850 = sum( np.abs(snd850 - nfs850) ) / (len(snd850))

MAE_thta_all_levs
MAE_thta_1000
MAE_thta_925
MAE_thta_850


MAPE_thta_all_levs = ( sum( np.abs( (sondes['THTA'] - naefs['THTA']) / sondes['THTA'] ) ) / (len(sondes['THTA'])) )*100
MAPE_thta_1000 = ( sum( np.abs( (snd1000 - nfs1000) / snd1000 ) ) / (len(snd1000)) )*100
MAPE_thta_925 = ( sum( np.abs( (snd925 - nfs925) / snd925 ) ) / (len(snd925)) )*100
MAPE_thta_850 = ( sum( np.abs( (snd850 - nfs850) / snd850 ) ) / (len(snd850)) )*100

MAPE_thta_all_levs
MAPE_thta_1000
MAPE_thta_925
MAPE_thta_850

# RMSE
RMSE_thta_all_levs = np.sqrt(sum( (sondes['THTA'] - naefs['THTA'])**2 / (len(sondes['THTA'])) )) 
RMSE_thta_1000 = np.sqrt(sum( (snd1000 - nfs1000)**2 / (len(snd1000)) )) 
RMSE_thta_925 = np.sqrt(sum( (snd925 - nfs925)**2 / (len(snd925)) )) 
RMSE_thta_850 = np.sqrt(sum( (snd850 - nfs850)**2 / (len(snd850)) )) 

RMSE_thta_all_levs
RMSE_thta_1000
RMSE_thta_925
RMSE_thta_850

# Correlations 
cor_all_levs = np.corrcoef(np.array(sondes['THTA']), np.array(naefs['THTA']))[0,1]
cor1000 = np.corrcoef(np.array(snd1000), np.array(nfs1000))[0,1]
cor925 = np.corrcoef(np.array(snd925), np.array(nfs925))[0,1]
cor850 = np.corrcoef(np.array(snd850), np.array(nfs850))[0,1]

cor_all_levs
cor1000
cor925 
cor850


# %% Correlation plot


fig, ax = plt.subplots(1,3, figsize=(15,5))
ax[0].scatter(np.array(snd1000), np.array(nfs1000), label = '1000 kPa')
ax[1].scatter(np.array(snd925), np.array(nfs925), label = '925 kPa')
ax[2].scatter(np.array(snd850), np.array(nfs850), label = '850 kPa')
ax[0].plot([280, 310], [280, 310], "r--")
ax[1].plot([280, 310], [280, 310], "r--")
ax[2].plot([280, 310], [280, 310], "r--")
ax[0].text(282,308, 'r = '+str(np.round(cor1000,2)), fontsize=12)
ax[1].text(282,308, 'r = '+str(np.round(cor925,2)), fontsize=12)
ax[2].text(282,308, 'r = '+str(np.round(cor850,2)), fontsize=12)
ax[0].set_xlim(280,310)
ax[1].set_xlim(280,310)
ax[2].set_xlim(280,310)
ax[0].set_ylim(280,310)
ax[1].set_ylim(280,310)
ax[2].set_ylim(280,310)

ax[0].set_ylabel('NAEFS - Potential Temperature (K)')

ax[0].set_title('1000 kPa')
ax[1].set_title('925 kPa')
ax[2].set_title('850 kPa')
ax[0].set_xlabel('Sondes - Potential Temperature (K)')
ax[1].set_xlabel('Sondes - Potential Temperature (K)')
ax[2].set_xlabel('Sondes - Potential Temperature (K)')

#plt.show()
plt.savefig(fig_dir+'correlation_thta'+run_date+'.png')



# %%

fig, ax = plt.subplots(1, figsize=(9,9))
ax.scatter(sondes['THTA'], naefs['THTA'], label = '1000 kPa')
ax.plot([280, 310], [280, 310], "r--")
ax.text(282,308, 'r = '+str(np.round(cor_all_levs,2)), fontsize=12)
ax.set_ylabel('NAEFS - Potential Temperature (K)')
ax.set_xlabel('Potential Temperature (K)')
ax.set_title('Correlation for potential temperature at all levels')
#plt.show()
plt.savefig(fig_dir+'correlation_thta_all_levs_'+run_date+'.png')


# %% try correlation of stabilties

np.corrcoef(sonde_stability_level_av_thta.unstack(),naefs_stability_level_av_thta.unstack())


# %%

sonde_stability_level_av_thta.unstack().mean(axis=1)
naefs_stability_level_av_thta.unstack().mean(axis=1)


# %%

fig, ax = plt.subplots(1,1, figsize=(15,5))
ax.scatter(np.array(sondes['THTA'][sondes['STABILITY']=='stable']), np.array(naefs['THTA'][naefs['STABILITY']=='stable']))


# %%
