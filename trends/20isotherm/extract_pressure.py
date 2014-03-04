import iris
import iris.analysis.maths as maths
import numpy as np
import os


def main():
    # We create a list of all of the files from which we wish to gather data
    file_stem = '/home/michael/Desktop/git/Masters/trends/20isotherm/'
    data_files_8n = os.listdir(file_stem + str(8))
    data_files_5n = os.listdir(file_stem + str(5))
    data_files_2n = os.listdir(file_stem + str(2))
    data_files_0n = os.listdir(file_stem + str(0)) 
    data_files_2s = os.listdir(file_stem + str(-2))
    data_files_5s = os.listdir(file_stem + str(-5))
    data_files_8s = os.listdir(file_stem + str(-8))
    
    all_files = [data_files_8n, data_files_5n, data_files_2n, data_files_0n,
                 data_files_2s, data_files_5s, data_files_8s]
    
    reference_lat = (8, 5, 2, 0, -2, -5, -8)
    reference_lon = (137, 147, 156, 165, 180, 190, 205, 220, 235, 250, 265)
    
    masked_value = -9.99
    
    raw_data_cube_list_2D = iris.cube.CubeList()
    anomoly_data_cube_list_2D = iris.cube.CubeList()
    monthly_average_cube_list_2D = iris.cube.CubeList()
    variation_data_cube_list_2D = iris.cube.CubeList()
    for index_lat in xrange(len(all_files)):
        raw_data_cube_list_1D = iris.cube.CubeList()
        monthly_average_cube_list_1D = iris.cube.CubeList()
        anomoly_data_cube_list_1D = iris.cube.CubeList()
        variation_data_cube_list_1D = iris.cube.CubeList()
        for index_lon in xrange(len(all_files[index_lat])):
            latitude = reference_lat[index_lat]
            longitude = reference_lon[index_lon]
            raw_data, anomoly_data, variation_data, monthly_average_data, time_points = extract_data(latitude, longitude, masked_value, file_stem)
            raw_data_cube = make_1D_cube(raw_data, 'time', time_points, latitude, longitude)
            anomoly_data_cube = make_1D_cube(anomoly_data, 'time', time_points, latitude, longitude)
            variation_data_cube = make_1D_cube(variation_data, 'time', time_points, latitude, longitude)
            monthly_average_data_cube = make_1D_cube(monthly_average_data, 'time', range(12), latitude, longitude)
            raw_data_cube_list_1D.append(raw_data_cube)
            anomoly_data_cube_list_1D.append(anomoly_data_cube)
            variation_data_cube_list_1D.append(variation_data_cube)
            monthly_average_cube_list_1D.append(monthly_average_data_cube)
        
        raw_data_merged_cube = raw_data_cube_list_1D.merge()[0]
        raw_data_cube_list_2D.append(raw_data_merged_cube)
        
        anomoly_data_merged_cube = anomoly_data_cube_list_1D.merge()[0]
        anomoly_data_cube_list_2D.append(anomoly_data_merged_cube)
        
        variation_data_merged_cube = variation_data_cube_list_1D.merge()[0]
        variation_data_cube_list_2D.append(variation_data_merged_cube)
        
        monthly_average_merged_cube = monthly_average_cube_list_1D.merge()[0]
        monthly_average_cube_list_2D.append(monthly_average_merged_cube)
   
    raw_data_cube = raw_data_cube_list_2D.merge()[0]
    raw_data_cube.rename('20C isotherm depth')
    
    anomoly_cube = anomoly_data_cube_list_2D.merge()[0]
    anomoly_cube.rename('20C isotherm depth anomoly')

    monthly_average_cube = monthly_average_cube_list_2D.merge()[0]
    monthly_average_cube.rename('Average 20C isotherm depth by month')
    
    average_temp_cube = raw_data_cube.collapsed('time', iris.analysis.MEAN)
    average_temp_cube.rename('Average 20C isotherm depth')
    
    variation_cube = variation_data_cube_list_2D.merge()[0]
    variation_cube.rename('20C isotherm depth variations')
    
    all_cubes = [raw_data_cube, monthly_average_cube, variation_cube, anomoly_cube, average_temp_cube]
    
    file_type = '.nc'
    filename = 'isotherm_cubes' + file_type
    
    iris.save(all_cubes, filename)
    print 'finished'
    
    
def extract_data(latitude, longitude, masked_value, file_stem):
    
    start_year = 1979
    end_year = 2013
    desired_column = 2
    tolerance = 0.1
    months = ('01', '02', '03', '04', '05', '06', 
              '07', '08', '09', '10' ,'11', '12')

    data = []
    
    filename = file_stem + str(latitude) + '/' + str(longitude) + '.txt'
    
    for year in xrange(start_year, end_year):
        for month in months:
            current_file = open(filename, 'r')
            date = ' ' + str(year) + month
            monthly_data = []
            for line in current_file:            
                if line.startswith(date):
                    values = line.split()
                    value = float(values[desired_column])
                    if not check_masked(value, masked_value, tolerance):
                        monthly_data.append(value)
            if len(monthly_data) == 0:
                monthly_average = masked_value
            else:
                monthly_average = np.mean(monthly_data)
            data.append(monthly_average)
    
    array = np.array(data)
    raw_data = np.ma.masked_values(array, masked_value, atol=tolerance)

    anomoly_data, variation_data, monthly_average_data = convert_to_anomoly(raw_data, masked_value, tolerance)

    number_of_points = (end_year - start_year) * 12
    time_points = range(number_of_points)
    
    print 'scanned ' + filename
    
    return raw_data, anomoly_data, variation_data, monthly_average_data, time_points


def check_masked(value, masked_value, tolerance):
    if value > (masked_value - tolerance) and value < (masked_value + tolerance):
        return True
    else:
        return False

def convert_to_anomoly(data_array, masked_value, tolerance):
    
    month_totals = ([],[],[],[],[],[],[],[],[],[],[],[])
    month_averages = []
    anomoly_data = []
    variation_data = []
    
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
            month_averages.append(masked_value)

    for (index, data_point) in enumerate(data_array):
        for counter in xrange(12):
            if (index+counter)%12 == 0:
                if data_point is np.ma.masked:
                    anomoly = masked_value
                    variation = masked_value
                else:
                    anomoly  = data_point - month_averages[counter]
                    variation = anomoly / month_averages[counter]
                    
                anomoly_data.append(anomoly)
                variation_data.append(variation)
    
    anomoly_array = np.array(anomoly_data)
    anomoly_array = np.ma.masked_values(anomoly_array, masked_value, atol=tolerance)
    
    variation_array = np.array(variation_data)
    variation_array = np.ma.masked_values(variation_array, masked_value, atol=tolerance)
    
    monthly_average_array = np.array(month_averages)
    monthly_average_array = np.ma.masked_values(month_averages, masked_value, atol=tolerance)
    
    return anomoly_array, variation_array, monthly_average_array



def get_expected_date(year_counter, month_counter):
    month_counter += 1
    if month_counter == 13:
        month_counter = 1
        year_counter += 1
    return str(year_counter) + str(month_counter)

            
def make_1D_cube(data, dim_name, dim_points, latitude, longitude):
    # This function makes a cube object out of the given data.

    cube_units = 'm'  
    cube_name = 'isotherm'

    # We collect information about the grid over which the data is collected
    if dim_name == 'time':
        dim_units = 'months'
    else:
        print 'unknown units... expected dimension of time.'
        dim_units = None
        
    dim_coord = iris.coords.DimCoord(dim_points, long_name=dim_name, units=dim_units)
    scaler_coord1 = iris.coords.AuxCoord([latitude], long_name = 'latitude', units='degrees')
    scaler_coord2 = iris.coords.AuxCoord([longitude], long_name = 'longitude', units='degrees')
    
    
    # We create the cube object    
    cube = iris.cube.Cube(data, long_name=cube_name, units=cube_units, dim_coords_and_dims=[(dim_coord, 0)]) 
    cube.add_aux_coord(scaler_coord1)
    cube.add_aux_coord(scaler_coord2)
    
    return cube


if __name__ == '__main__':
    main()