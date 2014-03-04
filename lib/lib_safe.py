import iris
import numpy as np
import iris.experimental.regrid as regrid
import matplotlib.pyplot as plt

def make_same_grid(source_cube, grid_cube, mode=None):
    '''
    Converts a cube with dimensions of latitude and longitude to have the same grid
    as the source cube. 
    '''
    
    new_cs = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
    
    source_cube.coord('latitude').coord_system = new_cs
    source_cube.coord('longitude').coord_system = new_cs
    grid_cube.coord('latitude').coord_system = new_cs
    grid_cube.coord('longitude').coord_system = new_cs
    
    if mode == None:
    
        size_source = source_cube.data.shape[0] * source_cube.data.shape[1]
        size_grid = grid_cube.data.shape[0] * grid_cube.data.shape[1]
        
        if size_source > size_grid:
            mode = 'weighted average'
        else:
            mode = 'linear interpolation'
            
    if mode == 'weighted average':
        
        source_cube.coord('latitude').guess_bounds()
        source_cube.coord('longitude').guess_bounds()
        grid_cube.coord('latitude').guess_bounds()
        grid_cube.coord('longitude').guess_bounds()
        
        regridded = regrid.regrid_area_weighted_rectilinear_src_and_grid(source_cube, grid_cube)
    
    else:
        regridded = regrid.regrid_bilinear_rectilinear_src_and_grid(source_cube, grid_cube)
    
    return regridded


def convert_to_csv(string):
    csv = ''
    character_present = False
    for character in string:
        if character == ' ':
            if character_present:
                csv += ','
            character_present = False
        else:
            csv += character
            character_present = True
    return csv


def force_maths(mode, cube_1, cube_2):
    
    cube_1 = cube_1 + 0
    cube_2 = cube_2 + 0
    
    latitude = cube_1.coord('latitude')
    longitude = cube_1.coord('longitude')
    
    cube_1.remove_coord('latitude')
    cube_2.remove_coord('latitude')
    cube_1.remove_coord('longitude')
    cube_2.remove_coord('longitude')
    
    if cube_1.units != cube_2.units:
        cube_1.units = None
        cube_2.units = None

    if mode == 'add':
        result = cube_1 + cube_2
        
    elif mode == 'subtract':
        result = cube_1 - cube_2
    
    elif mode == 'multiply':
        result = cube_1 * cube_2
    
    elif mode == 'divide':
        result = cube_1 / cube_2
        
    else:
        print 'mode not recognised'
        result = None
        
    result.add_dim_coord(latitude, 0)
    result.add_dim_coord(longitude, 1)
        
    return result

def calculate_pmcc(x_anomaly, y_anomaly, masked_value_x, masked_value_y):

    tol = 0.1

    if x_anomaly.shape != y_anomaly.shape:
        print 'Warning!!! cubes do not have the same shape'

    lat_points = x_anomaly.coord('latitude').points
    lon_points = x_anomaly.coord('longitude').points
    time_points = x_anomaly.coord('time').points

    pmcc_data = np.zeros((len(lat_points), len(lon_points)))

    for lat_index in xrange(len(lat_points)):
        for lon_index in xrange(len(lon_points)):
            reduced_x = x_anomaly[lat_index, lon_index]
            reduced_y = y_anomaly[lat_index, lon_index]
            n = 0.0
            covariance = 0.0
            sigma_x = 0.0
            sigma_y = 0.0
            for index in xrange(len(time_points)):
                if not reduced_x.data[index] is np.ma.masked:
                    if not reduced_y.data[index] is np.ma.masked:
                        n += 1
                        covariance += reduced_x.data[index] * reduced_y.data[index]
                        sigma_x += reduced_x.data[index]**2
                        sigma_y += reduced_y.data[index]**2
            if n != 0:
                covariance = covariance / n
                sigma_x = (sigma_x / n)**0.5
                sigma_y = (sigma_y / n)**0.5
                pmcc = covariance / (sigma_x * sigma_y)
            else:
                pmcc = masked_value_x
            pmcc_data[lat_index, lon_index] = pmcc
            print '(' + str(lat_points[lat_index]) + ',' + str(lon_points[lon_index]) + ')'
            
    pmcc_array = np.array(pmcc_data)
    pmcc_array = np.ma.masked_values(pmcc_array, masked_value_x, atol=tol)

    latitude = iris.coords.DimCoord(lat_points, long_name = 'latitude', units = 'degrees')
    longitude = iris.coords.DimCoord(lon_points, long_name = 'longitude', units = 'degrees')
    pmcc_cube = iris.cube.Cube(pmcc_array, long_name = 'pmcc', dim_coords_and_dims=[(latitude, 0), (longitude, 1)])

    pmcc_cube.rename('pmcc')
    
    return pmcc_cube
        

    