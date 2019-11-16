# E wicksteed

# November 2019

# get all the sounding data I need (for winter 2016)


from project.scripts.sondes.get_soundings2 import get_soundings
import requests
import pandas as pd
import numpy as np
import os


# set paths:
data_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/data/sondes/'
script_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/scripts/'

stn_no = '68816'
my_region = 'africa'

# yyyy = '2016'
# mm = '06'
# dd = '29'
# hh = '00'

# mm = ['06', '07', '08']

for year in range(2016, 2017):
    for month in range(6,9):
        month = str(month).zfill(2)
        for day in range(0,32):
            day = str(day).zfill(2)
            for hour in ['00', '12', '09']: # need to test if it works for any of these...
                print("download for "+str(year)+month+day+hour)
                get_soundings(year,month,day,hour,my_region,stn_no,data_dir)



get_soundings(2017,'06',29,00,my_region,stn_no,data_dir)


### need to test if website exists
import requests
request = requests.get('http://www.example.com')
if request.status_code == 200:
    print('Web site exists')
else:
    print('Web site does not exist') 