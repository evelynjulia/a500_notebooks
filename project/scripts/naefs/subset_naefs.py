# Eve Wicksteed
# November 2019
# Subset NAEFS grib files to a specific region

# need to have wgrib2 installed on computer

# imports
import glob
import os

# to list the files in my directories of each date

file_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/data/naefs/201606*/*'


def subset_naefs(latN, latS, lonW, lonE, region):

    '''

    Subsets naefs files in recursive directories to a certain defined region
    
    parameters
    ==========

    latN, 
    latS, 
    lonW, 
    lonE
    
    Returns
    =======

    grib files that are subsetted to bc with appended name of 'region'


    '''




    return None







list_of_files = glob.glob(file_dir)

for file in list_of_files:
    print(os.path.basename(file)+' in '+os.path.dirname(file))
    
