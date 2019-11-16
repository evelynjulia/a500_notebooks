# E wicksteed

# November 2019

# get all the sounding data I need (for winter 2016)



from get_soundings import get_soundings
import requests
import pandas as pd
import numpy as np
import os



# set paths:
data_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/data/sondes/'
script_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/scripts/'

stn_no = '68816'
my_region = 'africa'

yyyy = '2016'
mm = '06'
dd = '29'
hh = '00'

mm = ['06', '07', '08']

for i in range(0,32):
    i = str(i).zfill(2)
    print(i)


print(n.zfill(3))

get_soundings(yyyy,mm,dd,hh,my_region,stn_no,data_dir)