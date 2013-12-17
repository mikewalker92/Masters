import iris
import numpy as np

depth_points =  [1,5,10,20,40,60,80,100,120,140,180,300,500]
east_reading = [21.914, 21.772, 21.610, 21.145, 19.322, 16.624, 15.067, 14.329, 13.846, 13.489, 13.142,11.492,8.122]
west_reading = [22.602, 21.572, 20.091, 17.981, 15.889, 14.715, 14.096, 13.693, 13.469, 13.295, 13.127, 11.055,  7.935]

east_array = np.array(east_reading)
west_array = np.array(west_reading)

depth = iris.coords.DimCoord(depth_points, long_name = 'depth', units = 'm')

temp_east = iris.cube.Cube(east_array, long_name = 'east of basin temperature profile', units = 'celsius', dim_coords_and_dims = [(depth, 0)])
temp_west = iris.cube.Cube(west_array, long_name = 'west of basin temperature profile', units = 'celsius', dim_coords_and_dims = [(depth, 0)])

all_cubes = (temp_east, temp_west)

iris.save(all_cubes, 'temp_profiles.nc')
