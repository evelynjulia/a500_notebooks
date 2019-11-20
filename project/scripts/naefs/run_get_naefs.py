# eve wicksteed
# november 2019
# get naefs files from google drive by calling function

from project.scripts.naefs.get_naefs_bl import get_naefs
from os import path
import os

# get_naefs(year,month,day,hour,fcst_hr,mod,member,out_dir)

# set paths:
data_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/data/naefs/'

os.chdir(data_dir)

# set params:
mod = 'ncep'  # or cmc
member = 'gec00'


# year='2016'
# month='06'
# day='10'
hr = '00'

# init_date= year+month+day+hr
# fcsthr = '000'

for year in range(2016, 2017):
    for month in range(6, 9):
        month = str(month).zfill(2)
        for day in range(1, 32):
            day = str(day).zfill(2)
            for fcsthr in ['000', '006', '012', '018']:
                filepath = str(year)+month+day+hr+'/'+mod+'_'+member+'.t00z.pgrb2f'+fcsthr
                if path.exists(filepath):
                    print(filepath+' exists\n')
                else:
                    print(filepath+' does not exist')
                    print("download for "+str(year)+month+day+hr+' and for forecast hour '+fcsthr+'\n')
                    get_naefs(year, month, day, hr, fcsthr, mod, member, data_dir)
