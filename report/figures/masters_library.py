'''
This is a library of useful functions that are used frequently in the project.

It contains the following functions;

1 - extract_data()
1.1 - get_data()
1.2 - make_cube()
1.3 - check_masked()
2 - get_anomaly()
'''

import iris
import numpy as np
import iris.analysis.maths as math
import scipy.stats
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import scipy.interpolate
from scipy.fftpack import rfft, fftfreq

start_year = 1960

'''
--------------------------------------------------------------------------------
1. extract_data() - Assembles a cube from the data files
--------------------------------------------------------------------------------
'''

def extract_data(folder, mask, column):
    
    # State the grid over which the data is given.
    lat_points = (8, 5, 2, 0, -2, -5, -8)
    lon_points = (137, 147, 156, 165, 180, 190, 205, 220, 235, 250, 265)
    
    # We now can now loop through all of the grid points. We then merge all 
    # cubes at the same latitude, for each latitude, and then finally merge all
    # resulting cubes to obtain the full dataset. 
    
    data_cubelist_2d = iris.cube.CubeList()
    anomaly_cubelist_2d = iris.cube.CubeList()
    monthly_mean_cubelist_2d = iris.cube.CubeList()
    
    for latitude in lat_points:
        
        data_cubelist_1d = iris.cube.CubeList()
        anomaly_cubelist_1d = iris.cube.CubeList()
        monthly_mean_cubelist_1d = iris.cube.CubeList()
        
        for longitude in lon_points:
            
            data, time_points = get_data(latitude, longitude, mask, column, folder)
            anomaly, monthly_mean = get_anomaly(data, mask)
            
            data_cube = make_cube(data, time_points, latitude, longitude)
            anomaly_cube = make_cube(anomaly, time_points, latitude, longitude)
            monthly_mean_cube = make_cube(monthly_mean, range(12), latitude, longitude)
            
            data_cubelist_1d.append(data_cube)
            anomaly_cubelist_1d.append(anomaly_cube)
            monthly_mean_cubelist_1d.append(monthly_mean_cube)          
        
        merged_data = data_cubelist_1d.merge()[0]
        merged_anomaly = anomaly_cubelist_1d.merge()[0]
        merged_monthly_mean = monthly_mean_cubelist_1d.merge()[0]
        
        data_cubelist_2d.append(merged_data)
        anomaly_cubelist_2d.append(merged_anomaly)
        monthly_mean_cubelist_2d.append(merged_monthly_mean)
    
    data_cube = data_cubelist_2d.merge()[0]
    anomaly_cube = anomaly_cubelist_2d.merge()[0]
    monthly_mean_cube = monthly_mean_cubelist_2d.merge()[0]
    
    return [data_cube, anomaly_cube, monthly_mean_cube]

'''
--------------------------------------------------------------------------------
1.1 - get_data() - Fetches data from an individual file.
--------------------------------------------------------------------------------
'''

def get_data(latitude, longitude, mask, column, folder):
    
    end_year = 2012
    tolerance = 0.1
    months = ('01', '02', '03', '04', '05', '06',
              '07', '08', '09', '10', '11', '12')
    
    data = []
    
    filename = folder + '/' + str(latitude) + '/' + str(longitude) + '.txt'
    
    for year in xrange(start_year, end_year):
        for month in months:
            current_file = open(filename, 'r')
            date = ' ' + str(year) + month
            monthly_data = []
            for line in current_file:            
                if line.startswith(date):
                    values = line.split()
                    value = float(values[column])
                    if not check_masked(value, mask, tolerance):
                        monthly_data.append(value)
            if len(monthly_data) == 0:
                monthly_average = mask
            else:
                monthly_average = np.mean(monthly_data)
            data.append(monthly_average)

    array = np.array(data)
    data_array = np.ma.masked_values(array, mask, atol=tolerance)

    number_of_points = (end_year - start_year) * 12
    time_points = range(number_of_points)
    
    print 'scanned ' + filename
    
    return data_array, time_points

'''
--------------------------------------------------------------------------------
1.2 - make_cube() - Constructs a 1D cube from an array and a time_points
--------------------------------------------------------------------------------
'''

def make_cube(data, time_points, latitude, longitude):
    
    time = iris.coords.DimCoord(time_points, long_name='time', units='months')
    cube = iris.cube.Cube(data, dim_coords_and_dims=[(time, 0)])
    
    latitude = iris.coords.AuxCoord([latitude], long_name = 'latitude', units='degrees')
    longitude = iris.coords.AuxCoord([longitude], long_name = 'longitude', units='degrees')
    
    cube.add_aux_coord(latitude)
    cube.add_aux_coord(longitude)
    
    cube.rename('unknown')
    
    return cube

'''
--------------------------------------------------------------------------------
1.3 - check_masked() - Checks if the value matches the mask value.
--------------------------------------------------------------------------------
'''
    
def check_masked(value, mask, tolerance):
    if value > (mask - tolerance) and value < (mask + tolerance):
        return True
    else:
        return False

'''
--------------------------------------------------------------------------------
2 - get_anomaly() - converts the data cube into an anomaly cube. 
--------------------------------------------------------------------------------
'''

def get_anomaly(data_array, mask):
    
    tolerance = 0.1    
    month_totals = ([],[],[],[],[],[],[],[],[],[],[],[])
    month_averages = []
    anomaly_data = []
    
    for (index, data_point) in enumerate(data_array):
        for counter in xrange(12):
            if (index+counter)%12 == 0:
                if data_point is not np.ma.masked:
                    month_totals[counter].append(data_point)
                    
    for counter in xrange(12):
        if len(month_totals[counter]) != 0:
            ave = np.mean(month_totals[counter])
            month_averages.append(ave)
        else:
            month_averages.append(mask)

    for (index, data_point) in enumerate(data_array):
        for counter in xrange(12):
            if (index+counter)%12 == 0:
                if data_point is np.ma.masked:
                    value = mask 
                else:
                    value  = data_point - month_averages[counter]
                anomaly_data.append(value)             
    
    anomaly_array = np.array(anomaly_data)
    anomaly_array = np.ma.masked_values(anomaly_array, mask, atol=tolerance)
    
    month_averages = np.array(month_averages)
    month_averages = np.ma.masked_values(month_averages, mask, atol=tolerance)                              
    
    
    return anomaly_array, month_averages

'''
--------------------------------------------------------------------------------
3 - calculate_flux_full_data() - calculates the carbon flux from the data given.
--------------------------------------------------------------------------------
'''

def calculate_flux_full_data(data, const):
    
    # We first unpack the data
    
    sst = data[0]
    heat = data[1]
    wind = data[2]
    pressure = const['pressure_const']
    f = const['f']
    A = const['A']
    R = const['R']
    a = const['a']
    heat_ref = const['heat_ref']
    rho = const['rho']
    c = const['c']
    
    sst.units=None
    heat.units=None
    wind.units=None
    heat_ref.units=None
    
    # We now use the following equation to estimate the carbon flux;
    #
    # Flux = H*k*{Ae^(0.0423*T) - fP} + (70/44*rho*c)*R*(heat_ref - heat)
    #
    # where H = (1000/44*P)*(22.4 - 0.07T)
    #
    # and k = 87.6*(0.31v^2 - 0.71v + 7.76
    
    H = (1000./(44.*pressure)) * (-0.07*sst + 22.4 )
    k = 87.6*(0.31*wind**2 - 0.71*wind + 7.76)
    flux_sst = H*k*(A*math.exp(a*sst) - f*pressure)
    
    flux_upwelling = (70. * f * R * (-1.*heat + heat_ref)) / (44. * rho * c)
    
    flux = flux_sst + flux_upwelling
    
    return [flux, flux_sst, flux_upwelling]


'''
--------------------------------------------------------------------------------
4 - calculate_flux_iso_data() - calculates the carbon flux from the data given.
--------------------------------------------------------------------------------
'''

def calculate_flux_iso_data(isotherm, correlations, const):
    
    # We first unpack the data
    
    gradient_sst = correlations['gradient_sst']
    gradient_heat = correlations['gradient_heat']
    gradient_pressure = correlations['gradient_pressure']
    gradient_wind = correlations['gradient_wind']
    
    means_sst = correlations['means_sst']
    means_heat = correlations['means_heat']
    means_pressure = correlations['means_pressure']
    means_wind = correlations['means_wind']
    
    means_sst.units = None
    means_heat.units = None
    means_pressure.units = None
    means_wind.units = None
    
    f = const['f']
    A = const['A']
    R = const['R']
    a = const['a']
    heat_ref = const['heat_ref']
    pressure_const = const['pressure_const']
    rho = const['rho']
    c = const['c']
    
    # We now estimate the value of the variables from the value of the isotherm
    # depth using the expected value and the gradient obtained from the 
    # correlations.
    
    mask = -999.
    
    sst_data = []
    heat_data = []
    pressure_data = []
    wind_data = []
    
    heat_ref.units = None
    
    for time, datum in enumerate(isotherm.data):
        for counter in xrange(12):
            if (time+counter)%12 == 0:
                if datum is not np.ma.masked:
                    sst_data.append((means_sst[counter] + gradient_sst*datum).data)
                    heat_data.append((means_heat[counter] + gradient_heat*datum).data)
                    pressure_data.append((means_pressure[counter] + gradient_pressure*datum).data)
                    wind_data.append((means_wind[counter] + gradient_wind*datum).data)
                else:
                    sst_data.append(mask)
                    heat_data.append(mask)
                    pressure_data.append(mask)
                    wind_data.append(mask)
    
    time_points = isotherm.coord('time').points
    latitude = const['selected_lat']
    longitude = const['selected_lon']
    
    sst_data = np.ma.masked_values(sst_data, mask, atol=0.1)
    heat_data = np.ma.masked_values(heat_data, mask, atol=0.1)
    pressure_data = np.ma.masked_values(pressure_data, mask, atol=0.1)
    wind_data = np.ma.masked_values(wind_data, mask, atol=0.1)
    
    sst = make_cube(sst_data, time_points, latitude, longitude)
    heat = make_cube(heat_data, time_points, latitude, longitude)
    pressure = make_cube(pressure_data, time_points, latitude, longitude)
    wind = make_cube(wind_data, time_points, latitude, longitude)
    
    # We now use the following equation to estimate the carbon flux;
    #
    # Flux = H*k*{Ae^(0.0423*T) - fP} + (70/44*rho*c)*R*(heat_ref - heat)
    #
    # where H = (1000/44*P)*(22.4 - 0.07T)
    #
    # and k = 87.6*(0.31v^2 - 0.71v + 7.76
    
    H = (1000./(44.*pressure_const)) * (-0.07*sst + 22.4 )
    k = 87.6*(0.31*wind**2 - 0.71*wind + 7.76)
    pco2_ocean = A*math.exp(a*sst)
    pco2_ocean.units = None
    flux_sst = H*k*(pco2_ocean - f*pressure_const)
    
    flux_upwelling = (70. * f * R * (-1.*heat + heat_ref.data)) / (44. * rho * c)
    
    flux = flux_sst + flux_upwelling
        
    return [flux, flux_sst, flux_upwelling]


'''
--------------------------------------------------------------------------------
5 - get_correlations - returns the correlations between the variables.
--------------------------------------------------------------------------------
'''

def get_correlations(x, y):
    
    # We look for a correlation of the form y = mx + c
    #
    # We assume that c = 0 as we are dealing with perturbations from the mean.
    
    tol = 0.1
    mask = -999.
    
    if x.shape != y.shape:
        print 'Fatal Error: Variables do not have the same shape!'
        exit()

    lat_points = x.coord('latitude').points
    lon_points = x.coord('longitude').points
    time_points = x.coord('time').points

    pmcc_data = np.zeros((len(lat_points), len(lon_points)))
    gradient_data = np.zeros((len(lat_points), len(lon_points)))
    standard_error_data = np.zeros((len(lat_points), len(lon_points)))

    for lat_index in xrange(len(lat_points)):
        for lon_index in xrange(len(lon_points)):
            reduced_x = x[lat_index, lon_index]
            reduced_y = y[lat_index, lon_index]
            x_data = []
            y_data = []
            for index in xrange(len(time_points)):
                if reduced_x.data[index] is not np.ma.masked:
                    if reduced_y.data[index] is not np.ma.masked:
                        x_data.append(reduced_x.data[index])
                        y_data.append(reduced_y.data[index])
            if len(x_data) == 0 or len(y_data) == 0:
                pmcc = mask
                gradient = mask
                standard_error = mask
            else:
                gradient, _, pmcc, _, standard_error = scipy.stats.linregress(x_data, y_data)
            
            pmcc_data[lat_index, lon_index] = pmcc
            gradient_data[lat_index, lon_index] = gradient
            standard_error_data[lat_index, lon_index] = standard_error
            
    pmcc_array = np.array(pmcc_data)
    pmcc_array = np.ma.masked_values(pmcc_array, mask, atol=tol)
    
    gradient_array = np.array(gradient_data)
    gradient_array = np.ma.masked_values(gradient_array, mask, atol=tol)
    
    standard_error_array = np.array(standard_error_data)
    standard_error_array = np.ma.masked_values(standard_error_array, mask, atol=tol)

    latitude = iris.coords.DimCoord(lat_points, long_name = 'latitude', units = 'degrees')
    longitude = iris.coords.DimCoord(lon_points, long_name = 'longitude', units = 'degrees')
    
    pmcc_cube = iris.cube.Cube(pmcc_array, long_name = 'pmcc', dim_coords_and_dims=[(latitude, 0), (longitude, 1)])
    pmcc_cube.rename('pmcc')
    
    gradient_cube = iris.cube.Cube(gradient_array, long_name = 'gradient', dim_coords_and_dims=[(latitude, 0), (longitude, 1)])
    gradient_cube.rename('gradient')
    
    standard_error_cube = iris.cube.Cube(standard_error_array, long_name = 'standard_error', dim_coords_and_dims=[(latitude, 0), (longitude, 1)])
    standard_error_cube.rename('standard_error')
    
    return [pmcc_cube, gradient_cube, standard_error_cube]


def interpolate(cube):
    data_points = [0]
    data = [0]
    
    for index, value in enumerate(cube.data):
        if value is not np.ma.masked:
            data_points.append(index)
            data.append(value)
    f = scipy.interpolate.interp1d(data_points, data)
    
    return f

def get_fft(data, dt):
  
    fft = np.abs(rfft(data))**2
    rate = 180./dt
    x = [index*rate/len(data) for index in xrange(len(data))]
    x = np.array(x)

    return x, fft