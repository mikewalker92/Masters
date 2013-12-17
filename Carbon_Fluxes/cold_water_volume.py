import iris
import iris.analysis.maths as maths

'''
In this simple model, we shall assume that the amount of cold
water being advected is proportional to the difference between
the mesured heat and the expected heat. 
'''

measured_heat = iris.load('/home/michael/Desktop/git/Masters/Heat/Heat_cubes.nc')[2]
expected_heat = iris.load('/home/michael/Desktop/git/Masters/Heat/expected_heat.nc')[0]

volume_cold_water = maths.subtract(measured_heat, expected_heat)
volume_cold_water.rename('Cold Water Volume')
volume_cold_water.units = 'm3'

iris.save(volume_cold_water, 'volume_cold_water.nc')