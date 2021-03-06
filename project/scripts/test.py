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
#naefs_data_dir = "/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/"
naefs_data_dir = '/Users/ewicksteed/Documents/Eve/a500_notebooks_git_proj_version/project/data/'
naefs_files = "2016*/*SA.nc"

#sonde_data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'
sonde_data_dir = '/Users/ewicksteed/Documents/Eve/a500_notebooks_git_proj_version/project/data/sondes'
sonde_files = "*.csv"

dates_to_use = get_overlap_dates(naefs_dir= naefs_data_dir, naefs_files= naefs_files, sonde_dir = sonde_data_dir, sonde_files = sonde_files)

dates_pkl_file = open(data_dir+'dates_to_use.pkl', 'wb')
pickle.dump(dates_to_use, dates_pkl_file)
dates_pkl_file.close()

# pprint.pprint(sorted(dates_to_use))
# print(len(dates_to_use))


# test function to get sondes and plot 


#data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'
data_dir = '/Users/ewicksteed/Documents/Eve/a500_notebooks_git_proj_version/project/data/'
#fig_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/figures/'
fig_dir = '/Users/ewicksteed/Documents/Eve/a500_notebooks_git_proj_version/project/figures'

list_of_files = sorted(glob.glob('/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/*.csv'))

top_pres = 850
#stability_limit = 0.005 # what the cutoff is K/mb
stability_limit = 0.067 # what the cutoff is K/mb

# %%
#get_sonde_stabilty(data_dir, fig_dir, list_of_files, top_pres, stability_limit)


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
#p0=1.e5
p0 = 100 #kPa
Rd=287.  #J/kg/K
cpd=1004.  #J/kg/K
#CT_theta=CT_temp.variables.values*(p0/CT_press**(Rd/cpd))


naefs_df_tu =  pd.DataFrame()
naefs_df_tu['COMP_DATE'] = naefs_data['COMP_DATE'] 
naefs_df_tu['TMP1000'] = naefs_data['TMP1000']
naefs_df_tu['TMP925'] = naefs_data['TMP925']
naefs_df_tu['TMP850'] = naefs_data['TMP850']

# naefs_df_tu['THTA1000'] = naefs_df_tu['TMP1000']*((p0/100000)**(Rd/cpd))
# naefs_df_tu['THTA925'] = naefs_df_tu['TMP925']*((p0/100000)**(Rd/cpd))
# naefs_df_tu['THTA850'] = naefs_df_tu['TMP850']*((p0/100000)**(Rd/cpd))
# fix this 
naefs_df_tu['THTA1000'] = naefs_df_tu['TMP1000']*((p0/100)**(Rd/cpd))
naefs_df_tu['THTA925'] = naefs_df_tu['TMP925']*((p0/92.5)**(Rd/cpd))
naefs_df_tu['THTA850'] = naefs_df_tu['TMP850']*((p0/85)**(Rd/cpd))

#naefs_df_tu['AV_GRAD'] = (naefs_df_tu['THTA1000'] - naefs_df_tu['THTA850'])/150
#naefs_df_tu['AV_GRAD'] = ((naefs_df_tu['THTA1000'] - naefs_df_tu['THTA925'])/75 ) + ( (naefs_df_tu['THTA925'] - naefs_df_tu['THTA850'])/75 )
naefs_df_tu['AV_GRAD'] = ((naefs_df_tu['THTA925'] - naefs_df_tu['THTA1000'])/75 ) 

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
# 25 Jan 2020
# new sonde stability table

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
sonde_table_back = sonde_table_back.sort_values(by=['COMP_DATE', 'PRES'])
sonde_table_back = sonde_table_back.reset_index(drop=True)


sonde_new['AV_GRAD'] = sonde_table_back['value']


### done up to here 25 Jan 

stability_conditions = [
    sonde_new['AV_GRAD'] >= stability_limit,
    (sonde_new['AV_GRAD'] < stability_limit) & (sonde_new['AV_GRAD'] > -stability_limit),
    sonde_new['AV_GRAD'] <= -stability_limit ]

stability_choices = ['unstable', 'neutral', 'stable']  #['unstable', 'neutral', 'stable']
sonde_new['STABILITY'] = np.select(stability_conditions, stability_choices)

### GET TIME OF DAY COLUMN
sonde_new['TOD'] = sonde_new['COMP_DATE'].str[-2:]





###################################################################
# now make the sonde df exactly the same as the naefs one:
# df1_s = pd.DataFrame()
# df1_s['COMP_DATE'] = sonde_data_tu['COMP_DATE']
# df1_s['AV_GRAD'] = sonde_data_tu['THTA_GRAD_INTERP']
# df1_s['PRES'] = sonde_data_tu['PRES']
# df1_s['THTA'] = sonde_data_tu['THTA']
# df1_s['STABILITY'] = sonde_data_tu['STABILITY']
# df1_s['TOD'] = sonde_data_tu['TOD']

df1_s = pd.DataFrame()
df1_s['COMP_DATE'] = sonde_new['COMP_DATE']
df1_s['AV_GRAD'] = sonde_new['AV_GRAD']
df1_s['PRES'] = sonde_new['PRES']
df1_s['THTA'] = sonde_new['THTA']
df1_s['STABILITY'] = sonde_new['STABILITY']
df1_s['TOD'] = sonde_new['TOD']



df2_n = new_naefs_df_tu.copy()
#df2_n['THTA'] = df2_n['THTA'] #.round()

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

stab_sond_leg = ['Neutral', 'Stable', 'Unstable'] #['Neutral', 'Unstable', 'Stable']
#['Neutral', 'Stable', 'Unstable']
stab_naefs_leg = ['Neutral', 'Stable', 'Unstable']

fig, ax = plt.subplots(2,1, figsize=(15,9))
#plt.title('Mean theta by stability class')
ax[0].plot(sonde_stability_level_av_thta.unstack().iloc[0], Pres, color='green')
ax[0].plot(sonde_stability_level_av_thta.unstack().iloc[1], Pres, color='blue')
ax[0].plot(sonde_stability_level_av_thta.unstack().iloc[2], Pres, color='orange')
ax[1].plot(naefs_stability_level_av_thta.unstack().iloc[0], Pres, color='green')
ax[1].plot(naefs_stability_level_av_thta.unstack().iloc[1], Pres, color='blue')
ax[1].plot(naefs_stability_level_av_thta.unstack().iloc[2], Pres, color='orange')
ax[0].set_title('SONDES')
ax[1].set_title('NAEFS')
ax[0].set_xlim(277,300)
ax[1].set_xlim(277,300)
ax[0].set_ylabel('Pressure (kPa)')
#ax[0].set_xlabel('Theta')
ax[1].set_ylabel('Pressure (kPa)')
ax[1].set_xlabel('Potential temperature (K)')
ax[0].invert_yaxis()
ax[1].invert_yaxis()
ax[0].legend(stab_sond_leg)
ax[1].legend(stab_naefs_leg)
#plt.show()
plt.savefig(fig_dir+'Comparison_average_theta_by_stab_class'+run_date+'run_stablim'+str(stability_limit)+'.png')


fig, ax = plt.subplots(1,1, figsize=(15,9))
ax.plot(sonde_stability_level_av_thta.unstack().iloc[0], Pres, '-.', color='red')
ax.plot(sonde_stability_level_av_thta.unstack().iloc[1], Pres, color='red')
ax.plot(naefs_stability_level_av_thta.unstack().iloc[0], Pres, '-.', color='orange')
ax.plot(naefs_stability_level_av_thta.unstack().iloc[1], Pres, color='orange')
ax.set_xlim(280,300)
ax.set_ylabel('Pressure (kPa)')
ax.set_xlabel('Potential temperature (K)')
ax.invert_yaxis()
ax.legend(['Neutral - sonde', 'Stable - sonde', 'Neutral - NAEFS', 'Stable - NAEFS'])
#plt.show()
plt.savefig(fig_dir+'Comparison_average_theta_by_stab_class_all'+run_date+'run_stablim'+str(stability_limit)+'.png')



fig, ax = plt.subplots(2,1, figsize=(15,9))
ax[0].plot(sonde_lev_TOD_av.unstack().T.iloc[0], Pres)
ax[0].plot(sonde_lev_TOD_av.unstack().T.iloc[1], Pres)
ax[1].plot(naefs_lev_TOD_av.unstack().T.iloc[0], Pres)
ax[1].plot(naefs_lev_TOD_av.unstack().T.iloc[1], Pres)
ax[0].set_title('SONDES')
ax[1].set_title('NAEFS')
ax[0].set_ylabel('Pressure (kPa)')
ax[0].set_xlim(280,300)
ax[1].set_xlim(280,300)
#ax[0].set_xlabel('Theta')
ax[0].invert_yaxis()
ax[1].invert_yaxis()
ax[1].set_ylabel('Pressure (kPa)')
ax[1].set_xlabel('Potential temperature (K)')
ax[1].legend(tod)
ax[0].legend(tod)
#plt.title('Mean theta by time of sounding')
#plt.show()
plt.savefig(fig_dir+'Comparison_average_theta_by_TOD'+run_date+'run_stablim'+str(stability_limit)+'.png')


fig, ax = plt.subplots(1,1, figsize=(15,9))
ax.plot(sonde_lev_TOD_av.unstack().T.iloc[0], Pres, '-.', color='red')
ax.plot(sonde_lev_TOD_av.unstack().T.iloc[1], Pres, color='red')
ax.plot(naefs_lev_TOD_av.unstack().T.iloc[0], Pres, '-.', color='orange')
ax.plot(naefs_lev_TOD_av.unstack().T.iloc[1], Pres, color='orange')
ax.set_xlim(285,300)
ax.set_ylabel('Pressure (kPa)')
ax.set_xlabel('Potential temperature (K)')
ax.invert_yaxis()
ax.legend(['00 - sonde', '12 - sonde', '00 - NAEFS', '12 - NAEFS'])
#plt.show()
plt.savefig(fig_dir+'Comparison_average_theta_by_TOD_all'+run_date+'run_stablim'+str(stability_limit)+'.png')







#####################################################

df1_s
df2_n

# model error:

# set constants:
snd1000 = df1_s['THTA'][df1_s['PRES']==1000]
snd925 = df1_s['THTA'][df1_s['PRES']==925]
snd850 = df1_s['THTA'][df1_s['PRES']==850]
nfs1000 = df2_n['THTA'][df1_s['PRES']==1000]
nfs925 = df2_n['THTA'][df1_s['PRES']==925]
nfs850 = df2_n['THTA'][df1_s['PRES']==850]


# MAE: 
MAE_thta_all_levs = sum( np.abs(df1_s['THTA'] - df2_n['THTA']) ) / (len(df1_s['THTA']))
MAE_thta_1000 = sum( np.abs(snd1000 - nfs1000) ) / (len(snd1000))
MAE_thta_925 = sum( np.abs(snd925 - nfs925) ) / (len(snd925))
MAE_thta_850 = sum( np.abs(snd850 - nfs850) ) / (len(snd850))

MAE_thta_all_levs
MAE_thta_1000
MAE_thta_925
MAE_thta_850


MAPE_thta_all_levs = ( sum( np.abs( (df1_s['THTA'] - df2_n['THTA']) / df1_s['THTA'] ) ) / (len(df1_s['THTA'])) )*100
MAPE_thta_1000 = ( sum( np.abs( (snd1000 - nfs1000) / snd1000 ) ) / (len(snd1000)) )*100
MAPE_thta_925 = ( sum( np.abs( (snd925 - nfs925) / snd925 ) ) / (len(snd925)) )*100
MAPE_thta_850 = ( sum( np.abs( (snd850 - nfs850) / snd850 ) ) / (len(snd850)) )*100

MAPE_thta_all_levs
MAPE_thta_1000
MAPE_thta_925
MAPE_thta_850

# RMSE
RMSE_thta_all_levs = np.sqrt(sum( (df1_s['THTA'] - df2_n['THTA'])**2 / (len(df1_s['THTA'])) )) 
RMSE_thta_1000 = np.sqrt(sum( (snd1000 - nfs1000)**2 / (len(snd1000)) )) 
RMSE_thta_925 = np.sqrt(sum( (snd925 - nfs925)**2 / (len(snd925)) )) 
RMSE_thta_850 = np.sqrt(sum( (snd850 - nfs850)**2 / (len(snd850)) )) 

RMSE_thta_all_levs
RMSE_thta_1000
RMSE_thta_925
RMSE_thta_850

# Correlations 
cor_all_levs = np.corrcoef(np.array(df1_s['THTA']), np.array(df2_n['THTA']))[0,1]
cor1000 = np.corrcoef(np.array(snd1000), np.array(nfs1000))[0,1]
cor925 = np.corrcoef(np.array(snd925), np.array(nfs925))[0,1]
cor850 = np.corrcoef(np.array(snd850), np.array(nfs850))[0,1]

cor_all_levs
cor1000
cor925 
cor850




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
ax[0].set_title('SONDES')
ax[1].bar(df2_stability_keys, df2_stability_vals)
ax[1].set_ylabel('Count')
ax[1].set_xlabel('Stability class')
ax[1].set_title('NAEFS')
#ax[0].set_ylim(0,70)
#ax[1].set_ylim(0,70)
#ax[1].hist(snds_sm_dates.groupby('COMP_DATE').first()['MEAN_GRAD_BELOW_850'],50)
#ax[1].set_xlabel('Mean gradient between 1000mb and 850mb')
#plt.title('Number of cases in each stability class')
#plt.show()
plt.savefig(fig_dir+'bar_stab_classes_and_grad'+run_date+'run_stablim'+str(stability_limit)+'.png')








#### trying to recalculate the sonde gradients (the same way I calculated the naefs ones)

ptable = (df1_s.pivot(index = 'COMP_DATE', columns= 'PRES', values='THTA'))
test2 = (ptable[1000]-ptable[850])/150
plt.hist(test2)
plt.show()
#naefs_df_tu['AV_GRAD'] = (naefs_df_tu['THTA1000'] - naefs_df_tu['THTA850'])/150


##########################################################################################################

df1_s
df2_n

pres = [850,925,1000]

ptable_sondes = (df1_s.pivot(index = 'PRES', columns= 'COMP_DATE', values='THTA'))
ptable_naefs = (df2_n.pivot(index = 'PRES', columns= 'COMP_DATE', values='THTA'))

# plt.plot(ptable_sondes, pres)

# ptable2_naefs = (df2_n.pivot(index = 'COMP_DATE', columns= 'PRES', values='THTA'))
# plt.plot(ptable2_naefs.T) #, pres)
# plt.show()


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


# ###########################################################################################


# ####### trying to fix naefs stufF:
# new_df_plot = pd.DataFrame()
# new_df_plot['COMP_DATE'] = naefs_df_tu['COMP_DATE']
# new_df_plot['THTA1000'] = naefs_df_tu['THTA1000']
# new_df_plot['THTA925'] = naefs_df_tu['THTA925']
# new_df_plot['THTA850'] = naefs_df_tu['THTA850']
# new_df_plot = new_df_plot.set_index('COMP_DATE')



# # new_naefs_df_tu
# ptable_n2 = (new_naefs_df_tu.pivot(index = 'PRES', columns= 'COMP_DATE', values='THTA'))


# fig, ax = plt.subplots(1,1, figsize=(15,9))
# ax.plot(ptable_n2, pres)
# ax.set_title('NAEFS')
# ax.set_xlim(270,310)
# ax.invert_yaxis()
# plt.show()
# #plt.savefig(fig_dir+'actual_data_model_v_obs'+run_date+'.png')

# # df2_n
# ptable_n3 = (df2_n.pivot(index = 'PRES', columns= 'COMP_DATE', values='THTA'))


# fig, ax = plt.subplots(1,1, figsize=(15,9))
# ax.plot(ptable_n3, pres)
# ax.set_title('NAEFS')
# ax.set_xlim(270,310)
# ax.invert_yaxis()
# plt.show()




# pres2 = [1000,925,850]
# #run_date = dt.datetime.now().strftime('%y%m%d')

# fig, ax = plt.subplots(1,1, figsize=(15,9))
# ax.plot(new_df_plot.T, pres2)
# #ax.plot(new_naefs_test.T)
# ax.invert_yaxis()
# plt.title('NAEFS data')
# ax.set_xlabel('Potential temperature (K)')
# ax.set_ylabel('Pressure (kPa)')
# plt.show()
# #plt.savefig(fig_dir+'all_naefs_data_to_comp_overlapping_dates'+run_date+'run.png')



###########################################################################################
# # PLOT sondes verses naefs, original data

# fig, ax = plt.subplots(2,1, figsize=(15,9))
# ax[0].plot(ptable_sondes, pres)
# ax[1].plot(new_df_plot.T, pres2)
# ax[0].set_title('SONDES')
# ax[1].set_title('NAEFS')
# ax[0].set_xlim(270,310)
# ax[1].set_xlim(270,310)
# ax[0].set_ylabel('Pressure (kPa)')
# #ax[0].set_xlabel('Theta')
# ax[1].set_ylabel('Pressure (kPa)')
# ax[1].set_xlabel('Potential temperature (K)')
# ax[0].invert_yaxis()
# ax[1].invert_yaxis()
# #plt.show()
# plt.savefig(fig_dir+'actual_data_model_v_obs_attempt2'+run_date+'.png')
