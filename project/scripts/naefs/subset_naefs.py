# Eve Wicksteed
# November 2019
# Subset NAEFS grib files to a specific region

# need to have wgrib2 installed on computer

# imports
import glob
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
        print(os.path.basename(file)+' in '+os.path.dirname(file))
        subset_cmd = 'wgrib2 '+file+' -small_grib '+lonW+':'+lonE+' '+latS+':'+latN+' '+file+'_'+region
        #print(subset_cmd)
        os.system(subset_cmd)


    return None


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

# for file in list_of_files:
#     #print(os.path.basename(file)+' in '+os.path.dirname(file))
#     subset_cmd = 'wgrib2 '+file+' -small_grib '+my_lonW+':'+my_lonE+' '+my_latS+':'+my_latN+' '+file+'_'+my_region
#     print(subset_cmd)




#subset_cmd = 'wgrib2 '+file+' -small_grib '+lonE+':'+lonW+' '+latS+':'+latN+' '+file+'_'+region




