# Eve Wicksteed
# November 2019
# run program to convert grib files to netcdf files

# need to have wgrib2 installed on computer


# imports
import glob
from project.scripts.naefs.grib_to_nc import grib_to_nc

# get a list of all the files that I want to subset
my_file_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/data/naefs/2016*/*_SA'
my_list_of_files = glob.glob(my_file_dir)

# call function:
grib_to_nc(my_list_of_files)

