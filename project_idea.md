# ATSC 500 Project notes - Eve

31 October


# Project idea:
Understand model’s boundary layer scheme (maybe just pick one NAEFS model).
Compare this with sonde data (somewhere in the states where there is lots of data) and then compare with the soundings to see how well the model does at predicting the boundary layer.


## Questions:
- How many days of data do I need from the models?
- Would this be for cases? or for a long time series? eg. look at just he stable nocturnal boundary layer
  --> Would have to be for certain cases because I can't get a time series from sounding data
- Phil said something about predicting when the model will do well? Not sure about this… ask him maybe?
- Do I need to interpolate to a particular station?


## To do 
- Find 2 or 3 background papers that are topical 
- What are the key research papers in this particular area?
  eg. papers that have compared model boundary layer to obs and how do they compare? What are their metrics and statistical tests that they use?




# Project notes:

## See what variables are available in the model and how I could compare it:

**Data in NAEFS netCDF files:**

- Latent Heat Net Flux
- Sensible Heat Net Flux
- geopotential height at various levels
- U and V components of winds at various heights
- Temp at various heights
- relative humidity at various heights
- Vertical Velocity (Pressure) at 850mb
- precipitable water
- Pressure Reduced to MSL
- Total Cloud Cover
- Water Equivalent of Accumulated Snow Depth
- Snow Depth
- Min and Max temp


**About NAEFS model**

- American model is GFS and then has perturbations
- Canadian model is GEM and then has perturbations

So check the PBL scheme in these control members...




## Possible journal articles:
1. [Verification of Convection-Allowing WRF Model Forecasts of the Planetary Boundary Layer Using Sounding Observations](https://journals.ametsoc.org/doi/full/10.1175/WAF-D-12-00103.1)
  - Coniglio, M.C., J. Correia, P.T. Marsh, and F. Kong, 2013
  - They compare 5 PBL schemes in WRF to springtime radiosonde observations for deep convection events
  - Focus on the thermodynamic accuracy of the forecasts using radiosonde observations as truth.
  - They use Student's t-test to get statistical significance that the error is significantly different from zero. 
  - They look at the following things in terms of results and comparisons:
    * PBL height
    * Potential temperature profiles
    * Humidity profiles
    * Other derived sounding variables: e.g. CAPE, MLCAPE, MLCIN



# Deadline updates - 12 Nov

Understand forecast model boundary layer parameterization and compare with tower or sonde data

Have 3 papers and a dataset by Friday. So we will have 6 pages of setting and analysis and 6 pages of our own data analysis etc. 

What am I most interested in? wind? 

Could look at source code? (With Phil and Henryk)

Want to be able to see the monin-obukov equations and look at how they are implemented in the model
need to look at what equations are used for the boundary layer.

Phil's links:

  - [ARM site review paper](https://journals.ametsoc.org/doi/pdf/10.1175/AMSMONOGRAPHS-D-16-0004.1)

  - [FIFE](https://daac.ornl.gov/FIFE/guides/lidar_height_data.html)

  - [Gabls](https://link.springer.com/article/10.1007/s10546-014-9919-1)


Project code setup:

- Need to see tests with handwritten code
- Have some functions that you import into your notebook