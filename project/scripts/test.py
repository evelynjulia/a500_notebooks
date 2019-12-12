#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Eve Wicksteed
#
# 11 December 2019


# test getting overlapping dates

from project.scripts.functions import get_full_date
from project.scripts.functions import get_overlap_dates
import pprint
# import get_full_date(the_file)

naefs_data_dir = "/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/"
naefs_files = "2016*/*SA.nc"

sonde_data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'
sonde_files = "*.csv"

dates_to_use = get_overlap_dates(naefs_dir= naefs_data_dir, naefs_files= naefs_files, sonde_dir = sonde_data_dir, sonde_files = sonde_files)


pprint.pprint(sorted(dates_to_use))
print(len(dates_to_use))


# test function to get sondes and plot 

import glob
from project.scripts.sondes.function_to_get_sondes import get_sonde_stabilty

data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'
fig_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/figures/'

list_of_files = sorted(glob.glob('/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/*.csv'))

top_pres = 850
stability_limit = 0.005 # what the cutoff is K/mb

get_sonde_stabilty(data_dir, fig_dir, list_of_files, top_pres, stability_limit)

