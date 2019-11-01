# Project idea - Eve

31 October


project idea - understand model’s boundary layer scheme (maybe just pick one NAEFS model)
compare this with sonde data (somewhere in the states where there is lots of data) and then compare with the soundings to see how well the model does at predicting the boundary layer

see what variables are available in the model and how I could compare it. 

would this be for cases? or for a long time series?
eg. look at just he stable nocturnal boundary layer

Phil said something about predicting when the model will do well? Not sure about this… ask him maybe?


— NAPS —> national air pollution prevalence stations


** find 2 or 3 background papers that are topical 
what are the key research papers in this particular area
eg. papers that have compared model boundary layer to obs and how do they compare? what are their metrics and statistical tests that they use


In class we will learn how to work with 150G of data with x-array


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

