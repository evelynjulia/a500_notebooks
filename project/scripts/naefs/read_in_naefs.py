# Eve Wicksteed
#
# 22 November 2019

import glob
from netCDF4 import Dataset
import numpy as np
import datetime as dt
from a500.utils import ncdump
from netCDF4 import num2date, date2num
import pandas as pd
import os

import pickle


data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/'

list_of_files = glob.glob('/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/2016*/*.nc')


########################################################################
####################### Rodell's np array method #######################
########################################################################

#print(path_str[0][-8:-3])


#pathlist = sorted(Path(filein).glob(file+'*'))

hgt85, date = [], []
for file in list_of_files:
    print(os.path.basename(file)) # get the actual file name
    eves_file = Dataset(file,'r') 
    #print(eves_file.variables.keys())
    
    #hgt85_i = np.array(eves_file.variables['HGT_850mb'][0,...])
    hgt85_i = np.array(eves_file.variables['HGT_850mb'][0,...]).flatten() # to get a flat array

    time=eves_file.variables['time'][...]

    time_units= eves_file.variables['time'].units
    # get the date
    date_of_run = num2date(time,units=time_units)[0]
    date_i = dt.datetime.strftime(date_of_run,"%Y%m%d%H")
    print(date_i)

    hgt85.append(hgt85_i)
    date.append(date_i)


all_hgt85 = np.stack(hgt85)

# the above corresponds to the following date order
all_dates = np.stack(date)

########################################################################
######################## to pandas dataframe ########################
########################################################################

naefs_df_hgt85 = pd.DataFrame(all_hgt85.T, columns = all_dates)


file = open(data_dir+'naefs_df_hgt85.pkl', 'wb') # open a file, where you ant to store the data
pickle.dump(naefs_df_hgt85, file) # dump information to that file
file.close() # close the file