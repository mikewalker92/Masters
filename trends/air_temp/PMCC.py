import iris
import sys
sys.path.append('/home/michael/Desktop/git/Masters/lib')
import lib

'''
In this script, we will work out the PMCC for the correlation between this variable and 
the anomoly in the 20 isotherm height. 

We also calculate the linear regression using the scipy.stats.linregress method.
'''

def main():
    x_anomaly = iris.load('/home/michael/Desktop/git/Masters/trends/20isotherm/isotherm_cubes.nc')[2]
    y_anomaly = iris.load('/home/michael/Desktop/git/Masters/trends/air_temp/air_temp_cubes.nc')[0]  

    masked_value_x = -9.99
    masked_value_y = -9.99

    pmcc_cube, gradient_cube, intercept_cube, standard_error_cube = lib.calculate_pmcc(x_anomaly, y_anomaly, masked_value_x, masked_value_y)

    all_cubes = [pmcc_cube, gradient_cube, intercept_cube, standard_error_cube, x_anomaly, y_anomaly]
            
    iris.save(all_cubes, 'pmcc.nc')
    
if __name__ == '__main__':
    main()

