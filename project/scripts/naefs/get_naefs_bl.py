# eve wicksteed
# november 2019
# get naefs files from google drive

import os
#import h5py
#import pygrib
import subprocess
import numpy as np
#from glob import glob
#from os.path import isfile, basename
from datetime import datetime, timedelta


# work flow: copy from source --> unzip --> process and save
#source = '/Users/catherinemathews/Google Drive File Stream/Shared drives/Datamart/NAEFS/'
src_dir = '/Volumes/GoogleDrive/Shared drives/Datamart/NAEFS/'
data_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/data/naefs/'

# team_drive = '/glade/scratch/ksha/DATA/NAEFS/'      # source dir
# my_drive = '/glade/scratch/ksha/DATA/NAEFS_TEMP/'   # temporal space for un-ziping files
# local_space = '/glade/scratch/ksha/DATA/FILE_TEMP/' # storage of post-processed data

# range of dates to get files for
# Maybe do summer 2016?
dates = [datetime(2016, 1, 1, 0, 0)+timedelta(days=i) for i in range(365)] 

# 2016050900/cmc_gep20.t00z.pgrb2f132

# to extract certain file: 
#You can also use tar -zxvf <tar filename> <file you want to extract>

'''
untar_cmd = 'tar -zxvf '+ filename + file_to_extract -C path

'''

# test: 
#tar -zxvf /Users/catherinemathews/Google Drive File Stream/Shared drives/Datamart/NAEFS/2016050900.tgz 2016050900/ncep_gec00.t00z.pgrb2f000 - C /Users/catherinemathews/Google Drive File Stream/My Drive/Eve/data

#this works:
'tar -zxvf /Users/catherinemathews/Google\ Drive\ File\ Stream/Shared\ drives/Datamart/NAEFS/2016050900.tgz 2016050900/ncep_gec00.t00z.pgrb2f006 -C /Users/catherinemathews/Google\ Drive\ File\ Stream/My\ Drive/Eve/data/'


# where
# filename = date
# file_to_extract = ncep_gec00.t00z.pgrb2f{fcsthr}


#format in tarred folders: 
#2016050900/cmc_gep19.t00z.pgrb2f324



### get stuff ready for function

# change directory first
os.chdir(data_dir) # this isn't working

year='2016'
month='06'
day='10'
hr='00'

init_date= year+month+day+hr
fcsthr = '000'


tar_src_dir = '/Volumes/GoogleDrive/Shared\ drives/Datamart/NAEFS/'
tar_data_dir = '/Volumes/GoogleDrive/My\ Drive/Eve/courses/a500_notebooks_g/project/data/naefs/'


# remove file path because we're in the right directory
tar_cmd = 'tar -zxvf '+tar_src_dir+init_date+'.tgz '+init_date+'/ncep_gec00.t00z.pgrb2f'+fcsthr #+' -C '+data_dir

print('Getting data for '+init_date+' for fcst hour '+fcsthr)
subprocess.call(tar_cmd, shell=True) # test without this first: , shell=True)

'tar -zxvf /Volumes/GoogleDrive/Shared\ drives/Datamart/NAEFS/2016060100.tgz 2016060100/ncep_gec00.t00z.pgrb2f012 -C /Volumes/GoogleDrive/My\ Drive/Eve/courses/a500_notebooks_g/project/data/naefs/'



# Maybe I must change directories first?




#### Create function:

mod='ncep' # or cmc
member='gec00'


def get_naefs(year,month,day,hour,fcst_hr,mod,member,out_dir):

    """
    Gets NAEFS data for specific model, init time, forecast hour and model and member from 
    our google team drive and save to specified output directory
    
    parameters
    ==========

    year (YYYY): float or string
    month (MM): float or string
    day (DD): float or string
    hour (HH): float or string 
        initialization hour: we only download 00 
    
    mod: model (str)
        ncep (US) or cmc (Canadian)
    
    member: model member (str)



    out_dir: Directory into which to save the data 
        string
    
    Returns
    =======



    """

    # change dir because 'tar -C outdir' isn't working
    os.chdir(out_dir)

    # convert to strings
    year = str(year)
    month = str(month)
    day = str(day)
    hour = str(hour)


    # set full date string:
    date_str = year+month+day+hour

    # naefs source on team drive:
    src_dir = '/Volumes/GoogleDrive/Shared drives/Datamart/NAEFS/'

    # get / set column details
    col_names=['PRES','HGHT','TEMP','DWPT','RH','MIXR','WDIR','WSPD','THTA','THTE','THTV']
    col_widths=[7,7,7,7,7,7,7,7,7,7,7]
    cols_to_use = np.arange(0,len(col_names))
    rows_to_skip = 10
    foot_to_skip=60

    # read in dataframe using URL

    # check for website:
    request = requests.get(url)
    if request.status_code == 200:
        print('Web site exists')
        df = pd.read_fwf(url, skiprows=rows_to_skip, names=col_names, skipfooter=foot_to_skip, usecols=cols_to_use, widths=col_widths)
        
        # Add a date column to the dataframe
        df['DATE']= pd.to_datetime(year+month+day+' '+hour,format='%Y/%m/%d %H')

        # save as csv
        outfilename = date_str+'_sounding_'+stn+'.csv'

        df.to_csv(out_dir+outfilename)

        print('Saved to '+out_dir+' as '+ outfilename)
    
    else:
        print('Web site does not exist')
        print('No file for '+ date_str) 
        

    
    return None

