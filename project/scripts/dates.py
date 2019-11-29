# See which dates are the same for soundings and naefs
# 27 November
# EJW

from pathlib import Path
import re
import pprint
import os
import datetime



################################################################################################
#                                             NAEFS
################################################################################################


naefs_data_dir = "/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/"
all_naefs_files = list(Path(naefs_data_dir).glob("2016*/*SA.nc"))

####### SOME SORTING FUNCTIONS
find_hour = re.compile(r".*grb2.*(\d{3,3}).*_SA.nc")
find_date = re.compile(r".*naefs/*(\d{10,10}).*_SA.nc")

def get_full_date(the_file):
    """
    sort the files by converting the 10 digit initialization date to
    an integer and the 3 digit time to
    an integer and returning the combined initialization date and 
    forecast hour time so I can sort by both to read in my files
    """
    date_match = find_date.match(str(the_file))
    hour_match = find_hour.match(str(the_file))
    return int(date_match.group(1)[0:8]+hour_match.group(1)[1:])

# get list of dates:

all_naefs_dates = []
for file in all_naefs_files:
    date_i = get_full_date(file)
    all_naefs_dates.append(date_i)


#pprint.pprint(all_naefs_dates)




################################################################################################
#                                          SOUNDINGS
################################################################################################


sonde_data_dir = '/Users/catherinemathews/UBC/a500_notebooks/project/data/sondes/'
all_sonde_files = list(Path(sonde_data_dir).glob("*.csv"))

all_sonde_dates = []
for s_file in all_sonde_files:
    date_si = os.path.basename(s_file)[0:10]
    all_sonde_dates.append(int(date_si))



################################################################################################
#                                      COMPARE DATES
################################################################################################

# sort the dates so they're in the same order
sn_dates = sorted(all_naefs_dates)
ss_dates = sorted(all_sonde_dates)

comparison_set = set(sn_dates).intersection(ss_dates)

overlapping_dates = list(comparison_set)


################################################################################################
#                                    ALL DATES - PLOTTING
################################################################################################

# # new set with elements in sn_dates but not in ss_dates
# not_in_sondes = set(sn_dates).difference(ss_dates)


# # this has all the possible dates in it with no duplicates:
# all_dates = set(sn_dates).union(not_in_sondes)

# # create list of datetime objects
# new_date_l = []
# for i in list(all_dates):
#     ii = datetime.datetime.strptime(str(i), '%Y%m%d%H')
#     print(ii)
#     new_date_l.append(ii)


# # create list of 1 and 0 if dates exist
# test = list(all_dates.copy())
# for dt_ind, dt_val in enumerate(all_dates):
#     print(dt_ind)
#     print(dt_val)
#     if dt_val in overlapping_dates:  ### Figure out if it exists
#         print(dt_val in overlapping_dates)
#         print('date overlaps')
#         test[dt_ind] = 1
#     else:
#         test[dt_ind] = 0


