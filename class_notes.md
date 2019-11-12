---
title: Class notes
output: 
  html_document:
    keep_md: true
    theme: paper
    toc: true
---

# Table of contents
1. [10 Sep](# 10 September)


# ATSC 500 


# 10 September
	
create environmental variables so can just go `cd $a500`

can create functions to swap between condo versions


`mdfind -name stull | grep pdf`

`open <filename>`

the boundary layer has a well defined top which is because there is warm air descending that is dry because it’s all rained out in the hadley cell so that is why the top is defined

bjerknes slice theorem
- boundary layer at the equator is kind of created by clouds

important to look at spectra
- the relative something of high and low frequencies

Taylor’s hypothesis
if things aren’t time dependent (frozen turbulence) 
we can measure space by using change in time
fixed in space (eulerian) (uses PDEs) - we calculate in this
moving with flow (lagrangian) (uses proper derivatives, not partial) - we think in these


* check out the moira jardine slides:
https://www.dropbox.com/s/e2q2eruf7d0kk4w/fluids_01.pdf?dl=0
https://phaustin.github.io/a500web/docs/lec1_indepth.pdf
—> understand these!


can linearise a complicated equation by looking at different orders (e.g. in taylor series)
and then we use partial derivatives and we get some advection equation for lagrangian motion…


Readings for thursday
get from the equations: you can always reduce an average to calculus notation
read and be prepared to say something about them - the questions





# 12 September 

hackmd.io —> can use markdown and link to docs to ask questions
jupytext? to cover between notebooks and .py files

To test python from the command line

`python -c "import a500"`

when you call jupyter notebooks: 

`jupyter notebook &`

this will get it running in the background



`git fetch`


if we have made changes:

`git rebase origin/master`

copy notebook with our initials

if we haven’t made any edits:

`git reset —hard origin/master`


`pip install -e —upgrade` # apparently don’t need to do this anymore

pull combines fetch and rebase so better to do both separately


# 17 September

`killprocs python` —> this will kill all the python running process
get table of contents in j



Functions:

Docstring:

“””

A bit about what the function does

Parameters
- - - - -
param: file type
	what it does…

Returns
- - - - -
avg_var: float
	ensemble average of the variable
“””


# 19 September:


Type commands in the same order to update git repository 

`git fetch origin`

`git reset --hard origin/master`

`pip install -e . --upgrade`


Run to ensure you got the update 

`git log -1`




——

Think about what project I’d like to do (~35 hours of work) for this course. 


# 24 September

take home points from readings:
- term by term analysis of sinks and sources
- eg. page 142

get log normal distributions because you have variables multiplied by each other (multiplicative noise)
and take the log of them which is additive and then can use the central limit theorem which then gives us a log normal distribution

Phil’s notes are different in making hydrostatic perturbations



# 26 September

choose anelastic instead of boussinesq
so you can use bigger eddies and purturbations
the b. one resolves sound waves — and damps the waves so then don’t spread in the equation so you can use bigger time steps

b. doesn’t work for tropical convection apparently



reproduce velocity scale and then reproduce fire 4.18

[ars technica?](https://arstechnica.com/)





# 1 October

ln theta = entropy
pg. 174 —> once you have shear you can produce eddies and instabilities
1/4 the richardson number that is critical for overturning or something. see in “miles” notes
and see busing critical richardson number
richardson number goes down as kinetic energy goes up, high numbers, no turbulence


# 10 October 

`constrained_layout = True`

—> to make better plots

log normal —> nonlinear multiplicative sources
gaussian —> linear additive sources

mathpix


For funtions: 
can have info on arguments
parameters
and output


equations 11, 12 and 13
play around with subsidence rate and how you would scale it (cm/s) —> wh in eq. 12 from phil’s notes

account name and password for cedar account


# 15 October

`jupytext --to notebook spline_profiles.py  --execute`

don’t edit ipynb file
use 
`touch`

wh is negative?
gamma is the lapse rate

for the extra day put all three things on one graph

so put simple model on mixed layer model
dry les
flux profile
simple integrated
mixed layer
spline profiles

read to page 155

25 meters is too course to have the jump resolved
our eddies are too big that are entraining too much
Beta - 0.3 but should be 0.2?

things to compare
simple integration
mixed layer model
LES

get all on one page with 2 graphs for height of inversion and theta hat


use F0 as 60 if want it to match the dry les run

#############
https://docs.conda.io/en/latest/miniconda.html


## Installation and environment set up

Open a termnal with spotlight


`cd ~/Downloads`

`ls M*`

`bash Mini*`

`conda config --prepend channels conda-forge`

`conda install git`

`conda update --all`

`conda create -n ds --clone base`

`conda activate ds`

`conda install numpy scipy matplotlib`



`jupyter notebook`

`python -c "import a500"`



`cd ~/path of clone/`

`python -c "import package"`

`cd conda`

`conda env create -f environment.yml`


`conda activate a500test`

`pip install -e . --upgrade`



# 17 October

pick a month, 
log into cabauw
grap dataset
and figure out Obukohv length for your month
figure out stability
figure out fluxes
need to get account on cesar

boundary layer, meteo-> fluxes

helper functions are in a500 utils directory

non dimesional shear?

read chapter 6
For next Tuesday read Chapter 6 through section 6.5 and do problems 6.14, 6.15, 6.16, 6.17

-> about scaling stuff that we need to do

have project proposal by end of the month



# 23 October 2019

main thing about chapter 6 is using dyer stuff…
stratus to cumulous condition is where GCMs don’t do very well 


see cabau fit

stable 2am

sunrise 10am

full convection 2pm

overlay fit on curves


plot hist of obukhov length?

read phils essay plus fleagle and …

notebook for next tuesday


# 24 October 2019

most important equations are the ones in section 6.9 of fleagle businger…

the relationship between means and turbulence

in stable atmosphere there aren’t constant fluxes so we need to make corrections


how well does parameterisation do?


how do climate models handle clouds?





vs code

install >sshfs

project presentation - tuesday dec 3
deadline for project abstracts - next friday

Final project
10 -15 pages, 
4-6 figures, 
appendix?
notebook that shows work or the whole thing is a notebook



# 29 October 

Project notes:
(choose your own adventure)
obs or models
what to focus on : transport / structure…
scale dependence for a domain

du/dz increases with height by 5z/L when it’s non_dimensionalized with monin-obukhov theory

surface layer similarity is so important because it’s in every model

To update from a forked repo:

`git fetch upstream`

`git checkout master`

`git merge upstream/master`


parallelism
task based vs fork join



Optimum
ewicksteed@optimum.eos.ubc.ca 
Check www.optimum.eos.ubc.ca for docs (edited) 

 df -h
—> gives info on space

cmd shift p —> bring up palette on vs code


Ssh fs settings
host - optimum.eos.ubc.ca
port - 22
root - /home/


copy bash rc over



yppasswd
—> to change password

how to compile and run model ->

git clone dales les
https://github.com/phaustin/dales

cases is where all the model cases are…


mkdir build
cd build/

cmake ..
make j=4


dales_utils/dalesread coarse.py —> looks at data that phil got from a run

to get data use scp

need cisco so that we can pretend we’re on ubc secure to log into optimum

dales produces 2 files: profiles and time_ser


follow directions for optimum and dales this week


need to edit nameops for size of timestep 

name options shows everything you can do without recompiling the model


# 31 October

can’t use ordinary least squares if data is correlated in a time series.
so would have to do something with ARMA (auto regression - because it’s correlated to itself)
— use maximum likelihood instead

gaussian process regression…?
homoschedastic?

read pg. 312 on imaginary numbers in FFTs?


fourier transform the last code to check the cutoff points for the k/ power details after filtering. 


fft2d notebook --> have a class that carries around the data
intro to object orientated programming

now we have member functions and attributes for each object that we create...

power spectrum function adds info to the object (adds an attribute)


## For homework:

do what the cell is doing

photons in cloud travel further than 25 meters so when pixels talk to each other we get photon diffusion so we see the signature of that which is no longer tracking turbulence but mixing turbulent eddies from all over the cloud (200m) so we get diffusivity that looks like a k^2 terms


We need to filter the image and eliminate length scales smaller than 2km, back transform it and show the data
what radius in k space corresponds to 2km if pixel is 25m

k^2 = kx^2 + ky^2


filter, back transform

try on boundaries that aren't circular


# 5 November 2019

<!-- #region -->
decorators in python: higher order functions that contain other functions

Stallman created GNU and emacs

LLVM is the competitive compiler to GNU (then numba uses LLVM to run python fast)

Check the [nine rules of debugging](https://www.tygertec.com/9-rules-debugging/):
    - make it fail...?
   
Want the dissipation rate becaase it's the thing that's turning the eddies into heat.  (See fft_dissipation.py notebook)

xcorr_fft.py gives details on the size of eddies because if the plane flies and data is correlated over time then the air is related and probably in the same eddies. Uses this frozen turbulence theory?
    - Can use two ffts to get the autocorrelation
    
## Homework:

Go over these lectures from [ECMWF](https://confluence.ecmwf.int/display/OPTR/NWP+Training+Material+2019):
 - [PBL 1](https://www.dropbox.com/s/dcs4m640dxyg1t4/pbl1_is_2019.pdf?dl=0)
 - [PBL 2](https://www.dropbox.com/s/77owrwwanadmpw2/pbl2_is_2019.pdf?dl=0)
 - [PBL 3](https://www.dropbox.com/s/8gusigsskov4gbg/pbl3_is_2019.pdf?dl=0)
 

## Next week 

We'll look at the mixed layer but with the addition of evaporation and condensation
<!-- #endregion -->

# 7 November 2019


Installed beautiful soup

## Using pandas

`weather = pandas.read_csv(weather_file)`

`dir(weather)` --> this prints the list of things that can be down with the dataframe. Shows its methods

`weather.? <tab>` --> lists the functions that you can use

`import requests` --> get stuff from website programmatically

## For sonde data:
- [SHARPpy](https://github.com/sharppy/SHARPpy)
- [MetPy](https://unidata.github.io/python-gallery/examples/SkewT_Example.html#sphx-glr-examples-skewt-example-py)
- plus see Phil's wyoming notebook

## For easy access to Optimum:

[SSH Keygen](https://www.tecmint.com/ssh-passwordless-login-using-ssh-keygen-in-5-easy-steps/)


# 12 November 2019

## Project update:

Have 3 papers and a dataset by Friday

## Other notes:

Cloud stuff: 

- Have radiative cooling which changes fluxes... 
- Changes how surface affects the upper atmosphere
- Entrainment flux...?
- see thermo.pdf notes: don't want to use a dry theta that changes with evap etc. So we define theta_L that is conserved and doesn't change (conserves entropy)
- can convert between true entropy (`s` in 2nd law of thermodynamics) and the atmos entropy


See [thermlib.py](https://github.com/phaustin/a500_notebooks/blob/master/a500/thermo/thermlib.py):
- Can do a doc test with `>>>` in the docstring
- What is this testing? How do we do it? What's the point?
- [Pytest](https://docs.pytest.org/en/latest/)
- [Sphinx](http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)


Be able to publish a web page with docs about our functions in our library

`conda install sphinx`

`pip install sphinxcontrib-fulltoc`

copy `sphinx-build -N -v -b html . _build` to prompt and run it... 
- says build this website, build html, put in folder called build

Now we want to also be able to use [click](https://click.palletsprojects.com/en/7.x/documentation/):

- need to know whether you have options or arguments
- arguments are mandatory
- arguments don't have defaults

- would normally use parameters, results, etc for web things (see test_click.py)


If we're writing libraries we'll have tests and docstrings so they test themselves and document themselves.

## Homework:

- test the xarray dataset