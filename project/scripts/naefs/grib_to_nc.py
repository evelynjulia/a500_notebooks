# Eve Wicksteed
# November 2019
# Converts grib files to netcdf files

# need to have wgrib2 installed on computer

# imports
import os

def grib_to_nc(list_of_files):

    '''

    Subsets naefs files in recursive directories to a certain defined region
    
    parameters
    ==========

    list_of_files: list of files to iterate through
        list
    
    Returns
    =======

    grib files are converted to netcdf files


    '''

    for file in list_of_files:
        file_name = file.replace(' ', '\ ')
        convert_cmd = 'wgrib2 '+file_name+' -netcdf '+file_name+'.nc'
        os.system(convert_cmd)

    return None
