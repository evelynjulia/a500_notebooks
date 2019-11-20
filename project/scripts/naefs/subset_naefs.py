# Eve Wicksteed
# November 2019
# Subset NAEFS grib files to a specific region

# need to have wgrib2 installed on computer

# imports
import glob
import os

# to list the files in my directories of each date

my_file_dir = '/Volumes/GoogleDrive/My Drive/Eve/courses/a500_notebooks_g/project/data/naefs/201606*/*'


def subset_naefs(latN, latS, lonW, lonE, region, file_dir):

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
    
    file_dir: directory that holds all the files to iterate through
        this shouldn't have any files that you don't want to convert
        (str)
    
    Returns
    =======

    grib files that are subsetted to bc with appended name of 'region'


    '''

    latN = str(latN)
    latS = str(latS)
    lonW = str(lonW)
    lonE = str(lonE)

    list_of_files = glob.glob(file_dir)

    for file in list_of_files:
        print(os.path.basename(file)+' in '+os.path.dirname(file))
        subset_cmd = 'wgrib2 '+file+' -small_grib '+lonW+':'+lonE+' '+latS+':'+latN+' '+file+'_'+region
        #print(subset_cmd)
        os.system(subset_cmd)


    return None


# for cape town:
my_region = 'SA'
my_latN = '-20'
my_latS = '-35'
my_lonW = '15'
my_lonE = '35'

# call function:
subset_naefs(my_latN, my_latS, my_lonW, my_lonE, my_region, my_file_dir)

# for file in list_of_files:
#     #print(os.path.basename(file)+' in '+os.path.dirname(file))
#     subset_cmd = 'wgrib2 '+file+' -small_grib '+my_lonW+':'+my_lonE+' '+my_latS+':'+my_latN+' '+file+'_'+my_region
#     print(subset_cmd)




#subset_cmd = 'wgrib2 '+file+' -small_grib '+lonE+':'+lonW+' '+latS+':'+latN+' '+file+'_'+region




