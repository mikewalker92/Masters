import iris
import numpy as np
import math
import sys
sys.path.append('/home/michael/Desktop/git/Masters/lib')
import lib

'''
In this script, we will work out the PMCC for the correlation between this variable and 
the anomoly in the 20 isotherm height. 

We also calculate the linear regression using the scipy.stats.linregress method.
'''

def main():
    y_anomaly = iris.load('/home/michael/Desktop/git/Masters/trends/windspeed/windspeed_cubes.nc')[0]
    x_anomaly = iris.load('/home/michael/Desktop/git/Masters/trends/20isotherm/isotherm_cubes.nc')[2]
    
    masked_value_x = -99.9
    masked_value_y = -9.99
    
    pmcc_cube, gradient_cube, intercept_cube, standard_error_cube = lib.calculate_pmcc(x_anomaly, y_anomaly, masked_value_x, masked_value_y)
    
    all_cubes = [pmcc_cube, gradient_cube, intercept_cube, standard_error_cube, x_anomaly, y_anomaly]
    
    iris.save(all_cubes, 'pmcc.nc')
    
    
if __name__ == '__main__':
    main()
        
        