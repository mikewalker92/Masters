import iris
import iris.experimental.regrid
import numpy as np


upwelling = iris.load('/home/michael/Desktop/git/Masters/upflow/upwelling.nc')[0]
upwelling.rename('upwelling')

grid_latitude = []
grid_longitude = []

num_lat_points = 19
num_lon_points = 37

lat_gap = 180 / (num_lat_points - 1)
lon_gap = 360 / (num_lon_points - 1)

for counter in xrange(num_lat_points):
    point = counter * lat_gap - 90
    grid_latitude.append(point)
    
for counter in xrange(num_lon_points):
    point = counter * lon_gap
    grid_longitude.append(point)
    
new_cs = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
    
latitude = iris.coords.DimCoord(grid_latitude, standard_name = 'latitude', coord_system = new_cs, units = 'degrees')
longitude = iris.coords.DimCoord(grid_longitude, standard_name = 'longitude', coord_system = new_cs, units = 'degrees')

placeholder_data = np.zeros((num_lat_points, num_lon_points))

grid = iris.cube.Cube(placeholder_data, dim_coords_and_dims = [(latitude, 0), (longitude, 1)])
grid.rename('grid')

upwelling.coord('latitude').coord_system = new_cs
upwelling.coord('longitude').coord_system = new_cs

regridded = iris.experimental.regrid.regrid_bilinear_rectilinear_src_and_grid(upwelling, grid)
regridded.rename('regridded')

all_cubes = (regridded, grid, upwelling)

iris.save(all_cubes, 'regridded.nc')