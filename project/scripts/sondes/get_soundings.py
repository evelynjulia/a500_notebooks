
# E wicksteed
# November 2019
# to download sounding data



import requests
import pandas as pd
import numpy as np
import os


# set paths:
data_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/data/'
script_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/scripts/'

stn_no = '68816'
region = 'africa'
yyyy = '2019'
mm = '06'
dd = '29'
hh = '00'
# just want one sounding per file so have dd_start and stop be the same 
# and hh_start and stop are the same

start_url = 'http://weather.uwyo.edu/cgi-bin/sounding?region='


url = start_url+region+'&TYPE=TEXT%3ALIST&YEAR='+yyyy+'&MONTH='+mm+'&FROM='+dd+hh+'&TO='+dd+hh+'&STNM='+stn_no

#
r = requests.get(url, allow_redirects=True)
open(data_dir+'test_sounding.txt', 'wb').write(r.content)


#df = pd.read_fwf('test_sounding.txt',skiprows = 10, header =)
col_names=['PRES','HGHT','TEMP','DWPT','RH','W','WDIR','WSPD','THETA','THTE','THETV']
cols_to_use = np.arange(0,len(col_names))
df = pd.read_fwf(url, skiprows = 10, names=col_names, skipfooter= 60,usecols=cols_to_use,widths=[7,7,7,7,7,7,7,7,7,7,7])



# this is how to save to a csv file
df2.to_csv(data_dir+'test_save_df_as_csv.csv')





#np.genfromtxt(data_dir+'test_sounding.txt', skiprows=7, max_rows=1)



'''
create a function

want it to take in a list of URLS / or dates, region, times for soundings

read URLS into dataframe using pd.read_fwf:

extract the column names




'''