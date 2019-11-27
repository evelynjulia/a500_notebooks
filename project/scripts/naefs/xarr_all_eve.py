
import xarray
from netCDF4 import Dataset
from pathlib import Path
import context
from datetime import datetime
from pytz import utc
import matplotlib
from matplotlib import pyplot as plt
import pprint
import xarray as xr
matplotlib.use("Agg")
from a500.utils import ncdump
import re

#
# the following regular expression captures one group
# of exactly 3 characters, all numbers between 0-9
# the filenames look like ncep_gec00.t00z.pgrb2f006_SA.nc
#
find_hour = re.compile(r".*grb2.*(\d{3,3}).*_SA.nc")
#
#
#
# data_dir = "/scratch/paustin/ewicksteed/mydata/2016060100"
# all_files = list(Path(data_dir).glob("*.nc"))
# pprint.pprint(all_files)
data_dir = "/Users/catherinemathews/UBC/a500_notebooks/project/data/naefs/2016060100"

### so here I want to loop through all the folders (probably in order)
all_files = list(Path(data_dir).glob("*SA.nc"))
pprint.pprint(all_files)


def sort_hour(the_file):
    """
    sort the files by converting the 3 digit time to
    an integer and returning that number
    """
    the_match = find_hour.match(str(the_file))
    return int(the_match.group(1))

####### CREATE XARRAY
if __name__ == "__main__":
    all_files.sort(key=sort_hour)
    xarray_files = []
    for item in all_files:
        with Dataset(str(item)) as nc_file:
            the_time = nc_file.variables['time'][...]
            print(datetime.fromtimestamp(the_time, tz=utc))
            ds = xr.open_dataset(item)
            xarray_files.append(ds)
    ds_big = xr.combine_nested(xarray_files, 'time')

####### GET AVERAGE
    time_average = ds_big.mean('time') # this averages over all time so we 
    # get the daily average in this case (for 4 files) over all the lons and lats
    #
    # time_average.data_vars
    # time_average.coords


####### GET VARIABLE NAMES
    varnames = list(ds_big.variables.keys())
    

####### CREATE SMALLER XARRAY FOR ONE VARIABLE§    
    #
    #
    # create an xarray out of these files
    #
    vel_vals = [
        'VVEL_200mb', 'VVEL_250mb', 'VVEL_500mb', 'VVEL_700mb', 'VVEL_925mb',
        'VVEL_1000mb'
    ]
    vel_dict = {}
    for key in vel_vals:
        vel_dict[key] = ds_big.variables[key]
    ds_small = xr.Dataset(vel_dict, ds_big.coords)
    #
    # select a slice for the first timestep
    #
    out = ds_small['VVEL_200mb'].isel(time=0, latitude=slice(2, 4), longitude=slice(2,4))
    print(f"slice example {out}")
    ds_small.attrs[
        'history'] = f"written by {str(context.this_dir / 'eve_xarray.py')}"
    ds_small.to_zarr(context.data_dir / "small_wvel", 'w')





####### PLOTTING
    # #
    # # make a plot and copy it to you public web site
    # #
    # plot_var = ds_small['VVEL_925mb'].isel(time=0)
    # #plot_dir = Path().home() / "public_html" / "plot_dir"
    # plot_dir = Path().home() / "UBC" / "a500_notebooks" / "project" / "figures"
    # plot_dir.mkdir(parents=True, exist_ok=True)
    # print(f"creating {plot_dir}")
    # fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    # plot_name = "test.png"
    # ax.pcolormesh(ds_small.longitude,ds_small.latitude,plot_var)
    # ax.set(title = "VVEL_925mb", xlabel = "longitude", ylabel="latitude")
    # fig.savefig(plot_dir / plot_name)