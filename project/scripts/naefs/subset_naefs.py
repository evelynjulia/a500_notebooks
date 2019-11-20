# Eve Wicksteed
# November 2019
# Subset NAEFS grib files to a specific region

# need to have wgrib2 installed on computer

# imports
import os


def subset_naefs(latN, latS, lonW, lonE, region, list_of_files):

    '''

    Subsets naefs files in recursive directories to a certain defined region
    
    parameters
    ==========

    latN: north most latitude
        (int or str: will be converted to str)
    latS: south most latitude
        (int or str: will be converted to str)
    lonW: west most longitude
        (int or str: will be converted to str)
    lonE: east most longitude
        (int or str: will be converted to str)
    
    region: the name appended to the files
        (str)
    
    list_of_files: list of files to iterate through
        list
    
    Returns
    =======

    grib files that are subsetted to bc with appended name of 'region'


    '''

    latN = str(latN)
    latS = str(latS)
    lonW = str(lonW)
    lonE = str(lonE)

    for file in list_of_files:
        file_name = file.replace(' ', '\ ')
        subset_cmd = 'wgrib2 '+file_name+' -small_grib '+lonW+':'+lonE+' '+latS+':'+latN+' '+file_name+'_'+region
        os.system(subset_cmd)

    return None
