import iris

start_year = 1985
end_year = 2009
years = range(start_year, end_year + 1)
all_years = iris.cube.CubeList()

latitude_range = []
for i in xrange(180):
    latitude_range.append(-89.5 + i)
    
longitude_range = []
for j in xrange(360):
    longitude_range.append(0.5 + j)

latitude = iris.coords.DimCoord(latitude_range, standard_name = 'latitude', units = 'degrees')
longitude = iris.coords.DimCoord(longitude_range, standard_name = 'longitude', units = 'degrees')

for year in years:
    filename = 'qnet_' + str(year) + '.nc'
    cube = iris.load_cube(filename)
    averaged_cube = cube.collapsed('time', iris.analysis.MEAN)
    
    year_cube = iris.cube.Cube(averaged_cube.data, long_name = 'heat flux', units = 'W/m^2', dim_coords_and_dims=[(latitude, 0), (longitude, 1)])

    year_coord = iris.coords.AuxCoord([year], long_name = 'year')
    year_cube.add_aux_coord(year_coord)
    
    all_years.append(year_cube)
    
full_cube = all_years.merge()[0]

time_averaged = full_cube.collapsed('year', iris.analysis.MEAN)
time_averaged.rename('average from ' + str(start_year) + ' to ' + str(end_year))

time_averaged = time_averaged * -1

all_cubes = [time_averaged]

iris.save(all_cubes, 'heat_flux.nc')