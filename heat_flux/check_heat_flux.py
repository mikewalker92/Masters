import iris

import sys
sys.path.append('/home/michael/Desktop/git/Masters/lib')
import lib

'''
Here we check that the air-sea heat flux is proportional to air_temp - sea_temp

We will also wfind the constant of proportionality. 
'''

air_temp = iris.load_cube('/home/michael/Scitools/iris-sample-data/sample_data/air_temp.pp')
sea_temp = iris.load('/home/michael/Desktop/git/Masters/SST_daily/ersst.201201.nc')[0]
sea_temp = sea_temp[0,0]
actual = iris.load_cube('/home/michael/Desktop/git/Masters/heat_flux/heat_flux.nc')

air_temp = lib.make_same_grid(air_temp, sea_temp)

air_temp.convert_units('Celsius')
difference = sea_temp - air_temp
difference.rename('difference')

all_cubes = (air_temp, sea_temp, heat_flux, actual)

iris.save(all_cubes, 'check_heat_flux.nc')


                          