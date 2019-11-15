# eve wicksteed
# november 2019
# get naefs files from google drive

import os
import h5py
import pygrib
import subprocess
import numpy as np
from glob import glob
from os.path import isfile, basename
from datetime import datetime, timedelta


# work flow: copy from source --> unzip --> process and save
source = '/Users/catherinemathews/Google Drive File Stream/Shared drives/Datamart/NAEFS/'
temp_folder = '/Volumes/Scratch/ewicksteed/data/naefs/'
final_folder

team_drive = '/glade/scratch/ksha/DATA/NAEFS/'      # source dir
my_drive = '/glade/scratch/ksha/DATA/NAEFS_TEMP/'   # temporal space for un-ziping files
local_space = '/glade/scratch/ksha/DATA/FILE_TEMP/' # storage of post-processed data

# range of dates to get files for
# Maybe do summer 2016?
dates = [datetime(2016, 1, 1, 0, 0)+timedelta(days=i) for i in range(365)] 

2016050900/cmc_gep20.t00z.pgrb2f132

# to extract certain file: 
#You can also use tar -zxvf <tar filename> <file you want to extract>

untar_cmd = 'tar -zxvf '+ filename + file_to_extract -C path


# test: 
#tar -zxvf /Users/catherinemathews/Google Drive File Stream/Shared drives/Datamart/NAEFS/2016050900.tgz 2016050900/ncep_gec00.t00z.pgrb2f000 - C /Users/catherinemathews/Google Drive File Stream/My Drive/Eve/data

#this works:
'tar -zxvf /Users/catherinemathews/Google\ Drive\ File\ Stream/Shared\ drives/Datamart/NAEFS/2016050900.tgz 2016050900/ncep_gec00.t00z.pgrb2f006 -C /Users/catherinemathews/Google\ Drive\ File\ Stream/My\ Drive/Eve/data/'


# where
# filename = date
# file_to_extract = ncep_gec00.t00z.pgrb2f{fcsthr}


#format in tarred folders: 
#2016050900/cmc_gep19.t00z.pgrb2f324



