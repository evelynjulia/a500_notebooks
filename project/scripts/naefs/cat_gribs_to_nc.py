# Eve Wicksteed
# November 2019

import glob
import os
import subprocess


my_file_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/data/naefs/2016*/*006_SA.nc'
my_list_of_files = glob.glob(my_file_dir)
my_list_of_files = my_list_of_files.replace('/My Drive', '/My\ Drive')
# test  = my_list_of_files.replace('My Drive', 'My\ Drive')


# files_to_cat = ' '.join(my_list_of_files)
#files_to_cat = files_to_cat.replace('/My Drive', '/My\ Drive')


# outfile_name = '/Volumes/GoogleDrive/My\ Drive/Eve/courses/a500_notebooks_g/project/data/naefs/catted_grb'
# #cmd_cat_files = 'grib_copy '+files_to_cat+' '+outfile_name
# cmd_cat_files = 'cat '+files_to_cat+' > '+outfile_name



# for file in my_list_of_files:
#     file_name = file.replace(' ', '\ ')
#     cat_cmd = 'cat '+file_name+' /Volumes/GoogleDrive/My\ Drive/Eve/courses/a500_notebooks_g/project/data/naefs/catgrb > /Volumes/GoogleDrive/My\ Drive/Eve/courses/a500_notebooks_g/project/data/naefs/catgrb'
#     print(cat_cmd)
#     os.system(cat_cmd)


# os.system(cmd_cat_files)

# subprocess.call(cmd_cat_files)

import netCDF4
from netCDF4 import Dataset

f = netCDF4.MFDataset(my_list_of_files)

with Dataset(f):

with Dataset(f,'r') as ncin:
    lat=ncin.variables['latitude'][...]

print(f.variables["latitude"])


for nf in range(len(my_list_of_files)):
    with Dataset(my_list_of_files, "w", format='NETCDF4_CLASSIC') as f:
        f.createDimension("x",None)
        x = f.createVariable("x","i",("x",))
        x[0:10] = np.arange(nf*10,10*(nf+1))

f = netCDF4.MFDataset(my_list_of_files)

print(f.variables["x"][:])


ds = xarray.merge([xarray.open_dataset(f) for f in my_list_of_files])
ds = xarray.open_mfdataset('path/to/file/*.nc')
