'''
In this script, we generate usable data cubes from the raw data files. 

We do this for 5 data sets;

1. 20C isotherm depth
2. sst
3. heat content
4. pressure
5. wind speed

From each of these data sets, we obtain 3 cubes;

1. Monthly averaged time series.
2. Mean value for each month of the year. 
3. Monthly anomaly time series.
'''

'''
--------------------------------------------------------------------------------
Import the required modules
--------------------------------------------------------------------------------
'''

import iris

import masters_library as lib

'''
--------------------------------------------------------------------------------
We set the location of the folders for each of the data sets, + masked values.
--------------------------------------------------------------------------------
'''

isotherm_location = '/home/michael/git/Masters/trends/20isotherm'
sst_location = '/home/michael/git/Masters/trends/sst'
heat_location = '/home/michael/git/Masters/trends/heat'
pressure_location = '/home/michael/git/Masters/trends/pressure'
wind_location = '/home/michael/git/Masters/trends/windspeed'

mask_iso = -9.99
mask_sst = -9.99
mask_heat = -9.999
mask_pres = -9.90
mask_wind = -99.9

column_iso = 2
column_sst = 2
column_heat = 2
column_pres = 2
column_wind = 4

'''
--------------------------------------------------------------------------------
We now use our library of functions to help us extract the data from file.
--------------------------------------------------------------------------------
'''

isotherm_cubes = lib.extract_data(isotherm_location, mask_iso, column_iso)
sst_cubes = lib.extract_data(sst_location, mask_sst, column_sst)
heat_cubes = lib.extract_data(heat_location, mask_heat, column_heat)
pressure_cubes = lib.extract_data(pressure_location, mask_pres, column_pres)
wind_cubes = lib.extract_data(wind_location, mask_wind, column_wind)

for counter in xrange(3):
    heat_cubes[counter] = heat_cubes[counter] * 10.**10.
    pressure_cubes[counter] = pressure_cubes[counter] * 100.

'''
--------------------------------------------------------------------------------
We now set some properties of the cubes.
--------------------------------------------------------------------------------
'''

isotherm_cubes[0].rename('isotherm')
isotherm_cubes[1].rename('isotherm anomaly')
isotherm_cubes[2].rename('isotherm mean by month')

sst_cubes[0].rename('sst')
sst_cubes[1].rename('sst anomaly')
sst_cubes[2].rename('sst mean by month')

heat_cubes[0].rename('heat')
heat_cubes[1].rename('heat anomaly')
heat_cubes[2].rename('heat mean by month')

pressure_cubes[0].rename('pressure')
pressure_cubes[1].rename('pressure anomaly')
pressure_cubes[2].rename('pressure mean by month')

wind_cubes[0].rename('wind')
wind_cubes[1].rename('wind anomaly')
wind_cubes[2].rename('wind mean by month')

isotherm_cubes[0].units = 'm'
isotherm_cubes[1].units = 'm'
isotherm_cubes[2].units = 'm'

sst_cubes[0].units = 'Celsius'
sst_cubes[1].units = 'Kelvin'
sst_cubes[2].units = 'Celsius'

sst_cubes[0].convert_units('Kelvin')
sst_cubes[2].convert_units('Kelvin')

heat_cubes[0].units = 'J'
heat_cubes[1].units = 'J'
heat_cubes[2].units = 'J'

pressure_cubes[0].units = 'Pa'
pressure_cubes[1].units = 'Pa'
pressure_cubes[2].units = 'Pa'

wind_cubes[0].units = 'ms-1'
wind_cubes[1].units = 'ms-1'
wind_cubes[2].units = 'ms-1'

'''
--------------------------------------------------------------------------------
Finally, we save the generated cubes.
--------------------------------------------------------------------------------
'''

all_cubes = [isotherm_cubes[0], isotherm_cubes[1], isotherm_cubes[2],
             sst_cubes[0], sst_cubes[1], sst_cubes[2],
             heat_cubes[0], heat_cubes[1], heat_cubes[2],
             pressure_cubes[0], pressure_cubes[1], pressure_cubes[2],
             wind_cubes[0], wind_cubes[1], wind_cubes[2]]


iris.save(all_cubes, 'masters_data.nc')

