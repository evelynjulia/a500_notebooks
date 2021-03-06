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
- What am I most interested in? wind? 


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

[GFS operational physics](https://dtcenter.org/GMTB/gfs_phys_doc_dev/group___p_b_l.html)



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

2. [Implementation in the NCEP GFS of a Hybrid Eddy-Diffusivity Mass-Flux (EDMF) Boundary Layer Parameterization with Dissipative Heating and Modified Stable Boundary Layer Mixing](https://journals.ametsoc.org/doi/10.1175/WAF-D-15-0053.1?mobileUi=0)
  - Han, J., M.L. Witek, J. Teixeira, R. Sun, H. Pan, J.K. Fletcher, and C.S. Bretherton, 2016
  - Describes the boundary layer parameterization scheme in GFS
  - A new eddy-diffusivity mass-flux (EDMF) PBL scheme is developed
  -  EDMF scheme is applied only for the strongly unstable PBL
  - EDCG (eddy-diffusivity countergradient) scheme is used for the weakly unstable PBL
  - Heating by turbulent kinetic energy (TKE) dissipation is parameterized to reduce an energy imbalance in the GFS

  3. [Evaluation of Multiple Planetary Boundary Layer Parameterization Schemes in Southeast U.S. Cold Season Severe Thunderstorm Environments](https://journals.ametsoc.org/doi/full/10.1175/WAF-D-16-0193.1)
  - Cohen, A.E., S.M. Cavallo, M.C. Coniglio, H.E. Brooks, and I.L. Jirak, 2017
  - Compares various modelled PBL schemes with observational data in the US
  - low level wind profiles are important as well as low level thermodynamic profiles
  - uses 21 different severe weather events to compare

## Deadline updates - 12 Nov

**Goal:** Understand forecast model boundary layer parameterization and compare with tower or sonde data

Have 3 papers and a dataset by Friday. 


In the report we will have 6 pages of setting and analysis and 6 pages of our own data analysis etc. 
- Have 2 or 3 pages on the PBL scheme and how it works 
- have a season's worth of data



Could look at source code? (With Phil and Henryk):

- Want to be able to see the monin-obukov equations and look at how they are implemented in the model
need to look at what equations are used for the boundary layer.


One possible question to ask would be:  if the forecast model had matched the observed sounding exactly, how much of a difference would it have made in the surface fluxes as estimated by MO theory?

The nice thing about that is that if any information that you need is missing, you can just fill in an approximare guess and treat it as a sensitivity study.


**Phil's links:**

  - [ARM site review paper](https://journals.ametsoc.org/doi/pdf/10.1175/AMSMONOGRAPHS-D-16-0004.1)
  - [FIFE](https://daac.ornl.gov/FIFE/guides/lidar_height_data.html)
  - [Gabls](https://link.springer.com/article/10.1007/s10546-014-9919-1)


**Project code setup:**

- Need to see tests with handwritten code
- Have some functions that you import into your notebook


## Presentation

15 minutes: 12 mins for a talk and 3 mins questions

don't have more than 10 slides

- have research questions
- motivate what we're doing
- give plan for how we're tackling it. 
- show results if we have results
- transitions are important
- provide motivation, make sure it's doable and flag any issues. 


## 29 Nov notes: 

- https://atmos.washington.edu/~breth/classes/AS547/lect/lect8.pdf
- https://atmos.washington.edu/~breth/classes/AS547/

Chatted to Phil:

- first see which different stability classes (stable, convective, neutral) I have by looking at theta and the sign of the slope...
- the can create new columns in a pandas dataframe to classify the stabilty class and also the wind speed
- for wind speed can have a category of 1 for winds above 5m/s and 0 for winds under 5m/s
- then use groupby in pd. df to work with them. 
- can compare the model data to the stability class values to see if the same is represented
- want at least 10 examples in each category so I have a good RMS value


## 3 December notes

[Paper with classifications on stability classes](https://dc.uwm.edu/cgi/viewcontent.cgi?article=2458&context=etd)