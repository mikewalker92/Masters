import numpy as np
import iris

# This script create a cube from all the silly .txt files that matlab spits out

longitudefile = open('/home/michael/Desktop/git/Masters/upflow/longitudefile.txt')
longitudes = []
for line in longitudefile:
    longitudes.append(float(line))
longitudefile.close()

latitudefile = open('/home/michael/Desktop/git/Masters/upflow/latitudefile.txt')
latitudes = []
for line in latitudefile:
    latitudes.append(float(line))
latitudefile.close()

depthfile = open('/home/michael/Desktop/git/Masters/upflow/depthfile.txt')
depths = []
for line in depthfile:
    depths.append(float(line))
depthfile.close()

wfile = open('/home/michael/Desktop/git/Masters/upflow/wfile.txt')
data_list = []
for line in wfile:
    cells = line.split(',')
    values = []
    for cell in cells:
        if cell.startswith('NaN'):
            values.append(99.9)
        else:
            values.append(float(cell))
    array = np.array(values)  
    array = array.reshape(40, 216)
    data_list.append(array)

wfile.close()
data = np.dstack(data_list)
masked = np.ma.masked_values(data, 99.9, atol=0.1)

depth = iris.coords.DimCoord(depths, standard_name = 'depth', long_name = 'Depth', units = 'm')
latitude = iris.coords.DimCoord(latitudes, standard_name = 'latitude', long_name = 'latitute', units = 'degrees')
longitude = iris.coords.DimCoord(longitudes, standard_name = 'longitude', long_name = 'longitude', units = 'degrees')

upwelling = iris.cube.Cube(masked, long_name = 'Upwelling', units = None, dim_coords_and_dims=[(depth, 0),(latitude, 1),(longitude, 2)])

depth_average = upwelling.collapsed('depth', iris.analysis.MEAN)
depth_average.rename('average over depth')

all_cubes = [upwelling, depth_average]

iris.save(all_cubes, 'upwelling.nc')


