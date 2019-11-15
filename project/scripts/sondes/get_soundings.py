
# E wicksteed
# November 2019
# to download sounding data



import requests




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


r = requests.get(url, allow_redirects=True)
open('test_sounding.txt', 'wb').write(r.content)

import pandas as pd
df = pd.read_fwf('test_sounding.txt',skiprows = 10, header =)

df2 = pd.read_fwf(url)


'''
create a function

want it to take in a list of URLS / or dates, region, times for soundings

read URLS into dataframe using pd.read_fwf:

extract the column names




'''