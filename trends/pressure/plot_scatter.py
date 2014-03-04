import iris
import sys
sys.path.append('/home/michael/Desktop/git/Masters/lib')
import lib
import numpy as np

cubes = iris.load('/home/michael/Desktop/git/Masters/trends/pressure/pmcc.nc')

x_anomoly = cubes[0]
y_anomoly = cubes[3]
gradient = cubes[2]
intercept = cubes[4]

# we now choose a latitude and longitude to examine closer. 

lat_index = 3
lon_index = 9

x_anomoly = x_anomoly[3,9]
y_anomoly = y_anomoly[3,9]
gradient = gradient.data[3,9]
intercept = intercept.data[3,9]  

x_data = []
y_data = []
time_points = x_anomoly.coord('time').points

for point in xrange(len(time_points)):
    if not x_anomoly.data[point] is np.ma.masked:
        if not y_anomoly.data[point] is np.ma.masked:
            x_data.append(x_anomoly.data[point])
            y_data.append(y_anomoly.data[point])

lib.plot_scatter(x_data, y_data, gradient, intercept)