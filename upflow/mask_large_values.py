
import iris
import numpy as np
import math


upwelling = iris.load('/home/michael/Desktop/git/Masters/upflow/upwelling.nc')[0]

shape = upwelling.data.shape

w = np.zeros(shape)

for i in xrange(shape[0]):
    for j in xrange(shape[1]):
        if upwelling.data[i,j] > 0.0002 or upwelling.data[i,j] < -0.0002 or math.isnan(upwelling.data[i,j]):
            w[i,j] = 99.9
        else:
            w[i,j] = upwelling.data[i,j]

w = np.ma.masked_values(w, 99.9, atol=0.1)

latitude = upwelling.coord('latitude')
longitude = upwelling.coord('longitude')
masked_upwelling = iris.cube.Cube(w, long_name = 'masked upwelling',  dim_coords_and_dims = [(latitude, 0), (longitude, 1)])

all_cubes = [upwelling, masked_upwelling]

iris.save(all_cubes, 'masked_large.nc')