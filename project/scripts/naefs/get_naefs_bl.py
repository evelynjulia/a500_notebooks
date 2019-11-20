# eve wicksteed
# november 2019
# get naefs files from google drive

import os
import subprocess
import numpy as np
from datetime import datetime, timedelta


#src_dir = '/Volumes/GoogleDrive/Shared drives/Datamart/NAEFS/'
#data_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/data/naefs/'


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
        gec00 for control
        oe gep01 to 20

    out_dir: Directory into which to save the data 
        string
    
    Returns
    =======

    Downloaded NAEFS files for certain dates/times/models


    """

    # change dir because 'tar -C outdir' isn't working
    os.chdir(out_dir)

    # convert to strings
    year = str(year)
    month = str(month)
    day = str(day)
    hour = str(hour)
    fcst_hr=str(fcst_hr)

    # set full date string:
    init_date = year+month+day+hour

    # naefs source on team drive:
    tar_src_dir = '/Volumes/GoogleDrive/Shared\ drives/Datamart/NAEFS/'

    # Create tar command
    tar_cmd = 'tar -zxvf '+tar_src_dir+init_date+'.tgz '+init_date+'/'+mod+'_'+member+'.t'+hour+'z.pgrb2f'+fcst_hr

    # extract files
    print('Getting data for '+init_date+' for fcst hour '+fcst_hr)
    print('Downloading file '+mod+'_'+member+'.t'+hour+'z.pgrb2f'+fcst_hr)
    subprocess.call(tar_cmd, shell=True) 


    return None

