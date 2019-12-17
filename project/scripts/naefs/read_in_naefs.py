# Eve Wicksteed
#
# 22 November 2019

import glob
from netCDF4 import Dataset
import numpy as np
import datetime as dt
from a500.utils import ncdump
from netCDF4 import num2date, date2num
import pandas as pd
import os

import pickle


data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/'

list_of_files = glob.glob('/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/2016*/*.nc')



#print(path_str[0][-8:-3])

########################################################################
#######################     Get dates to use     #######################
########################################################################

from project.scripts.functions import get_full_date
from project.scripts.functions import get_overlap_dates
import pprint
# import get_full_date(the_file)
naefs_data_dir = "/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/"
naefs_files = "2016*/*SA.nc"
sonde_data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'
sonde_files = "*.csv"
dates_to_use = get_overlap_dates(naefs_dir= naefs_data_dir, naefs_files= naefs_files, sonde_dir = sonde_data_dir, sonde_files = sonde_files)
#pprint.pprint(sorted(dates_to_use))


########################################################################
####################### Rodell's np array method #######################
########################################################################
#pathlist = sorted(Path(filein).glob(file+'*'))


# get lat and lon index
# CAPE TOWN
# 33.9249° S, 18.4241° E
choose_lat = -33
choose_lon = 18 


temp_file = Dataset(list_of_files[0],'r') 
lon = temp_file.variables['longitude'][...]
lat = temp_file.variables['latitude'][...]
lon_ew = lon.copy()
lon_ew[lon_ew > 180] = lon_ew[lon_ew > 180]-360

# need to get index where lat = choose_lat and where lon = choose_lon
which_lon = lon_ew # if initially just eastings
#which_lon = lon # or lon if eastings and westings

lat_ind = np.where(lat == choose_lat)
lon_ind = np.where(which_lon == choose_lon)

print("latitude and longitude indices")
print(lat_ind, lon_ind)


hgt850, hgt925, hgt1000, date, tmp850, tmp925, tmp1000 = [], [], [], [], [], [], []
rh1000, rh925, rh850, vvel1000 = [],[],[],[]
for file in sorted(list_of_files):
    print(os.path.basename(file)) # get the actual file name
    eves_file = Dataset(file,'r') 
    #print(eves_file.variables.keys())
    
    # get the date
    time=eves_file.variables['time'][...]

    time_units= eves_file.variables['time'].units
    date_of_run = num2date(time,units=time_units)[0]
    date_i = dt.datetime.strftime(date_of_run,"%Y%m%d%H")
    print(date_i)

    if int(date_i) in dates_to_use:
        print(date_i, 'in dates to use')
        date.append(date_i)

        # get other variables
        #hgt85_i = np.array(eves_file.variables['HGT_850mb'][0,...])[lat_ind, lon_ind] # to get data for CT
        hgt850_i = float(eves_file.variables['HGT_850mb'][0,...][lat_ind, lon_ind]) # to get data for CT
        hgt925_i = float(eves_file.variables['HGT_925mb'][0,...][lat_ind, lon_ind])
        hgt1000_i = float(eves_file.variables['HGT_1000mb'][0,...][lat_ind, lon_ind])
        tmp1000_i = float(eves_file.variables['TMP_1000mb'][0,...][lat_ind, lon_ind])
        tmp925_i = float(eves_file.variables['TMP_925mb'][0,...][lat_ind, lon_ind])
        tmp850_i = float(eves_file.variables['TMP_850mb'][0,...][lat_ind, lon_ind])
        rh1000_i = float(eves_file.variables['RH_1000mb'][0,...][lat_ind, lon_ind])
        rh925_i = float(eves_file.variables['RH_925mb'][0,...][lat_ind, lon_ind])
        rh850_i = float(eves_file.variables['RH_850mb'][0,...][lat_ind, lon_ind])
        vvel1000_i = float(eves_file.variables['VVEL_1000mb'][0,...][lat_ind, lon_ind])
        
        hgt850.append(hgt850_i)
        hgt925.append(hgt925_i)
        hgt1000.append(hgt1000_i)
        tmp1000.append(tmp1000_i)
        tmp925.append(tmp925_i)
        tmp850.append(tmp850_i)
        rh1000.append(rh1000_i)
        rh925.append(rh925_i)
        rh850.append(rh850_i)
        vvel1000.append(vvel1000_i)

    else:
        pass





all_naefs_data = pd.DataFrame()
all_naefs_data['COMP_DATE'] = date
all_naefs_data['HGT850'] = hgt850
all_naefs_data['HGT925'] = hgt925
all_naefs_data['HGT1000'] = hgt1000
all_naefs_data['TMP1000'] = tmp1000
all_naefs_data['TMP925'] = tmp925
all_naefs_data['TMP850'] = tmp850
all_naefs_data['RH1000'] = rh1000
all_naefs_data['RH925'] = rh925
all_naefs_data['RH850'] = rh850
all_naefs_data['VVEL1000'] = vvel1000


########################################################################
######################## to pandas dataframe ########################
########################################################################


file = open(data_dir+'all_naefs_df.pkl', 'wb') # open a file, where you ant to store the data
pickle.dump(all_naefs_data, file) # dump information to that file
file.close() # close the file

# naefs_df_hgt85 = pd.DataFrame(all_hgt85.T, columns = all_dates)
# file = open(data_dir+'naefs_df_hgt85.pkl', 'wb') # open a file, where you ant to store the data
# pickle.dump(naefs_df_hgt85, file) # dump information to that file
# file.close() # close the file