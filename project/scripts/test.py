

from project.scripts.functions import get_full_date
from project.scripts.functions import get_overlap_dates
import pprint
# import get_full_date(the_file)

naefs_data_dir = "/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/"
naefs_files = "2016*/*SA.nc"

sonde_data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'
sonde_files = "*.csv"

test_func = get_overlap_dates(naefs_dir= naefs_data_dir, naefs_files= naefs_files, sonde_dir = sonde_data_dir, sonde_files = sonde_files)


pprint.pprint(sorted(test_func))