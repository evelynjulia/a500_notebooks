# Eve Wicksteed
# November 2019

import glob
import os


my_file_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/data/naefs/2016*/*_SA'
my_list_of_files = glob.glob(my_file_dir)

test  = my_list_of_files.replace('My Drive', 'My\ Drive')


files_to_cat = ' '.join(my_list_of_files)
files_to_cat =files_to_cat.replace('/My Drive', '/My\ Drive')


outfile_name= 'catted_grb'
cmd_cat_files = 'grib_copy '+files_to_cat+outfile_name



