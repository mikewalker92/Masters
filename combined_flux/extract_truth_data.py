import iris
import numpy as np
import sys
sys.path.append('/home/michael/Desktop/git/Masters/lib')
import lib
filename = '/home/michael/Desktop/git/Masters/combined_flux/truth_data.txt'

data = []

data_file = open(filename)
for line in data_file:
    if not line.startswith('LAT'):
        line = lib.convert_to_csv(line)
        cells = line.split(',')
        data.append((cells[0], cells[1], cells[5]))

lat_points = []
lon_points = []

for i in xrange(45):
    lat_points.append(-88 + i*4)

for j in xrange(72):
    lon_points.append(2.5 + j*5)

data_shape = np.zeros((45,72))
flux = np.ma.masked_values(data_shape, 0, atol = 0.1)
            
for point in data:
    i = (float(point[0]) + 88) / 4.0
    j = (float(point[1]) -2.5) / 5.0
    flux[i,j] = float(point[2])

latitude = iris.coords.DimCoord(lat_points, long_name = 'latitude', units = 'degrees')
longitude = iris.coords.DimCoord(lon_points, long_name = 'longitude', units = 'degrees')

flux_cube = iris.cube.Cube(flux, long_name = 'truth flux', units = 'mol / m^2 yr', dim_coords_and_dims = [(latitude, 0), (longitude, 1)])

iris.save(flux_cube, 'true_flux.nc')

    