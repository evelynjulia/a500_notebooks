# Eve Wicksteed
# November 2019
# run program to subset NAEFS grib files to a specific region

# need to have wgrib2 installed on computer


# imports
import glob
# import os
from project.scripts.naefs.subset_naefs import subset_naefs

# get a list of all the files that I want to subset
my_file_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/data/naefs/2016*/*'
my_list_of_files = glob.glob(my_file_dir)

# for cape town:
my_region = 'SA'
my_latN = '-20'
my_latS = '-35'
my_lonW = '15'
my_lonE = '35'

# call function:
subset_naefs(my_latN, my_latS, my_lonW, my_lonE, my_region, my_list_of_files)



