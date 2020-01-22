
# %%

from project.scripts.functions import get_full_date
from project.scripts.functions import get_overlap_dates
#from functions import get_full_date
#from functions import get_overlap_dates
import pprint
# import get_full_date(the_file)

import glob
from project.scripts.sondes.function_to_get_sondes import get_sonde_stabilty
#from sondes.function_to_get_sondes import get_sonde_stabilty

import pickle

import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

import pandas as pd

# %%

naefs_data_dir = "/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/"
data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'
fig_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/figures/'

pkl_file = open(naefs_data_dir+'all_naefs_df.pkl', 'rb') 
naefs_data = pickle.load(pkl_file) 
pkl_file.close() 

# %%
p0=1.e5
Rd=287.  #J/kg/K
cpd=1004.  #J/kg/K
#naefs_df_tu['TMP1000']*((p0/100000)**(Rd/cpd))

new_naefs_test = pd.DataFrame()
new_naefs_test['COMP_DATE'] = naefs_data['COMP_DATE']
new_naefs_test['THTA1000'] = naefs_data['TMP1000']*((p0/100000)**(Rd/cpd))
new_naefs_test['THTA925'] = naefs_data['TMP925']*((p0/100000)**(Rd/cpd))
new_naefs_test['THTA850'] = naefs_data['TMP850']*((p0/100000)**(Rd/cpd))

new_naefs_test = new_naefs_test.set_index('COMP_DATE') #, columns= ('THTA1000', 'THTA925', 'THTA850'))

pres = [1000,925,850]
run_date = dt.datetime.now().strftime('%y%m%d')

fig, ax = plt.subplots(1,1, figsize=(15,9))
ax.plot(new_naefs_test.T, pres)
#ax.plot(new_naefs_test.T)
ax.invert_yaxis()
plt.title('NAEFS data')
ax.set_xlabel('Potential temperature (K)')
ax.set_ylabel('Pressure (kPa)')
#plt.show()
plt.savefig(fig_dir+'all_naefs_data_to_comp_overlapping_dates'+run_date+'run.png')

new_naefs_test


#ptable_naefs = (naefs_data.pivot(index = 'PRES', columns= 'COMP_DATE', values='THTA'))