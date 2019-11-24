# Eve Wicksteed
#
# 23 November 2019

import glob
from netCDF4 import Dataset
import numpy as np
import datetime as dt
from a500.utils import ncdump
from netCDF4 import num2date, date2num
import pandas as pd
import os

import pickle


data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'

list_of_files = glob.glob('/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/*.csv')

# get date
for file in list_of_files:
    print(file)
    #print(os.path.basename(file))
    