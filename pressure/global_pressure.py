import iris

pressure_cube = iris.load('/home/michael/Desktop/git/Masters/pressure/slp.1999.nc')[1]

average_pressure = pressure_cube.collapsed('time', iris.analysis.MEAN)

iris.save(average_pressure, 'pressure.nc')