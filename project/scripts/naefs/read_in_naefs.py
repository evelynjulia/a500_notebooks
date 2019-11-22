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

data_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/data/naefs/'
date_of_run = num2date(time,units=time_units)[0]

list_of_files = glob.glob('/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/data/naefs/2016*/*.nc')



df = pd.DataFrame()
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

