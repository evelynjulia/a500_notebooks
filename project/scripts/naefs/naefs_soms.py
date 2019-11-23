# Eve Wicksteed
# 22 November 2019
# get SOMs of my data


# now we want to unravel the array so we can feed it into SOMS
# first unravel each day
# then combine all into one 2D array with rows as data and columns as the 
# lat and lon vars that have been flattened
# then can feed into minisom SOM package 

import pickle
from minisom import MiniSom
import numpy as np

data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/'
filename = 'naefs_df_hgt85.pkl'



# OPEN THE DATA
pkl_file = open(data_dir+filename, 'rb') # open a file, where you stored the pickled data
my_data = pickle.load(pkl_file) # dump information to that file
pkl_file.close() # close the file

data_arr = np.array(my_data)
 
test_som = MiniSom(4,3,my_data.shape[1])
test_som.train_random(data_arr, 10, verbose=True)

wmap = test_som.win_map(data_arr)