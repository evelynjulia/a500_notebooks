# Eve Wicksteed
#
# 22 November 2019

import glob
from netCDF4 import Dataset
import numpy as np
import datetime as dt
from a500.utils import ncdump
#import matplotlib.pyplot as plt
from netCDF4 import num2date, date2num
import pandas as pd

import os
from pathlib import Path

#data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/'
#date_of_run = num2date(time,units=time_units)[0]

list_of_files = glob.glob('/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/2016*/*.nc')


########################################################################
######################## Eve's dataframe method ########################
########################################################################
#df = pd.DataFrame()

for file in list_of_files[0:3]:
    #print(file)
    with Dataset(file,'r') as gec00:
        hgt85 = gec00.variables['HGT_850mb'][0,...] # .byteswap().newbyteorder()
        time=gec00.variables['time'][...]
        time_units= gec00.variables['time'].units
        flat_hgt85 = hgt85.flatten()# .byteswap().newbyteorder()
        # get the date
        date_of_run = num2date(time,units=time_units)[0]
        date = dt.strftime(date_of_run,"%Y%m%d%H")
        print(date)
    # add data to a pd df with date as the column name
    df[date] = flat_hgt85


########################################################################
######################## Chris' np array method ########################
########################################################################

#print(path_str[0][-8:-3])


pathlist = sorted(Path(filein).glob(file+'*'))

hgt85 = []
for path in list_of_files[0:3]:
    #print(os.path.basename(path)) # get the actual file name
    eves_file = Dataset(path,'r') 
    #print(eves_file.variables.keys())
    
    #hgt85_i = np.array(eves_file.variables['HGT_850mb'][0,...])
    # to get a flat array
    hgt85_i = np.array(eves_file.variables['HGT_850mb'][0,...]).flatten() 
    print(len(hgt85_i))
    print(hgt85_i.shape)
    #rh.append(rh_i)
    hgt85.append(hgt85_i)
    


hgt85_stack = np.stack(hgt85)

#hgt85_stack.shape

    
