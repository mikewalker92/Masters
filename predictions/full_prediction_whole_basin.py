'''
our model assumes that the total flux is made up of 2 components, 
a flux due to the partial pressures in the ocean and the air, which 
is driven by the sea surface temperature. The second component is a 
carbon flux due to the upwelling cold carbon rich water from the deep
ocean. 

total_flux = flux_sst + flux_upwelling

flux_sst = H*k*delta_pCO2

flux_upwelling = w*delta_concentration
'''

import iris

'''
We first load the El Nino parameter. In this case we will use the 20 degree
isotherm depth anomaly as an analog for the strength of El Nino.
'''
isotherm_anomaly = iris.load('/home/michael/Desktop/git/Masters/trends/20isotherm/isotherm_cubes.nc')[5]
isotherm_anomaly.rename('isotherm_anomaly')
isotherm_anomaly.coord('time').units='months'
isotherm_anomaly.units='m'


'''
We will now aproximate all other variables as;
    
    x = <x> + a*isotherm_anomaly
    
where <x> is the mean of x. We must therefore also load cubes representing
the mean value of each variable. Further, we have 
'''

sst_mean_cube = iris.load('/home/michael/Desktop/git/Masters/trends/sst/sst_cubes.nc')[0]
windspeed_mean_cube = iris.load('/home/michael/Desktop/git/Masters/trends/windspeed/windspeed_cubes.nc')[4]
heat_mean_cube = iris.load('/home/michael/Desktop/git/Masters/trends/heat/heat_cubes.nc')[4]

sst_gradient_cube = iris.load('/home/michael/Desktop/git/Masters/trends/sst/pmcc.nc')[2]
windspeed_gradient_cube = iris.load('/home/michael/Desktop/git/Masters/trends/windspeed/pmcc.nc')[2]
heat_gradient_cube = iris.load('/home/michael/Desktop/git/Masters/trends/heat/pmcc.nc')[2]

sst_mean = sst_mean_cube
pressure_mean = 1005.
windspeed_mean = windspeed_mean_cube
heat_mean = heat_mean_cube

sst_mean.units = None
windspeed_mean.units = None
heat_mean.units = None

sst_gradient = sst_gradient_cube
pressure_gradient = 0.
windspeed_gradient = windspeed_gradient_cube
heat_gradient = heat_gradient_cube

'''
We now define some parameters of the model
'''

A = 1.283e-4
R = 400.
f = 380e-6
delta_T = 5
expected_heat = heat_mean_cube.data[0,4] * 10.**10.
time_step = 1./12.

'''
and some constants
'''
a = 0.0423
specific_heat = 4.18e6
water_density = 1000.

'''
We are now able to construct our aproximate variables based on the isotherm 
anomaly.
'''
flux_list = iris.cube.CubeList()
sst_flux_list = iris.cube.CubeList()
upwelling_flux_list = iris.cube.CubeList()
time_points = isotherm_anomaly.coord('time').points
for index in xrange(len(time_points)):
    
    sst = sst_mean + sst_gradient*isotherm_anomaly[:,:,index]
    pressure = (pressure_mean + pressure_gradient*isotherm_anomaly[:,:,index]) * 100
    windspeed = windspeed_mean + windspeed_gradient*isotherm_anomaly[:,:,index]
    heat = (heat_mean + heat_gradient*isotherm_anomaly[:,:,index]) *10.**10.

    sst.units=None
    pressure.units=None
    windspeed.units=None
    heat.units=None

    sst.rename('sst')
    pressure.rename('pressure')
    windspeed.rename('windspeed')
    heat.rename('heat')


    '''
    Here we calculate the flux due to the SST
    '''
    pCO2_ocean = A*iris.analysis.maths.exp(a*sst)
    pCO2_ocean.rename('pCO2_ocean')
    pCO2_ocean.units=None
    pCO2_air = f*pressure
    pCO2_air.rename('pCO2_air')

    delta_pCO2 = pCO2_ocean - pCO2_air
    delta_pCO2.rename('delta_pCO2')

    S = -1*(0.07*sst - 22.4) * (1000./44.) * f
    H = S / pCO2_air
    H.rename('H')

    k = 86.7*(0.31*windspeed**2 - 0.71*windspeed + 7.76)

    flux_sst = H*k*delta_pCO2
    flux_sst.rename('flux from sst')


    '''
    Here we calculate the flux due to upwelling
    '''

    missing_heat = -1*(heat - expected_heat)
    cold_water_volume = missing_heat / (specific_heat*water_density*delta_T)
    cold_water_volume.rename('cold water volume')
    upwelling = (R*cold_water_volume) / time_step

    delta_concentration = (70./44.)*delta_T*f

    flux_upwelling = upwelling*delta_concentration
    flux_upwelling.rename('flux from upwelling')

    '''
    Finally, we can obtain the total flux
    '''

    flux = flux_sst + flux_upwelling
    
    time = iris.coords.AuxCoord([index], long_name='time')
    
    flux.add_aux_coord(time)
    flux.attributes=None
    flux_list.append(flux)
    
    flux_sst.add_aux_coord(time)
    flux_sst.attributes=None
    sst_flux_list.append(flux_sst)
    
    flux_upwelling.add_aux_coord(time)
    flux_upwelling.attributes=None
    upwelling_flux_list.append(flux_upwelling)

    
flux_cube = flux_list.merge()[0]
flux_cube.rename('total flux')
flux_average = flux_cube.collapsed('time', iris.analysis.MEAN)
flux_average.rename('average total flux')

sst_flux_cube = sst_flux_list.merge()[0]
flux_sst = sst_flux_cube.collapsed('time', iris.analysis.MEAN)
flux_sst.rename('sst flux')

upwelling_flux_cube = upwelling_flux_list.merge()[0]
flux_upwelling = upwelling_flux_cube.collapsed('time', iris.analysis.MEAN)
flux_upwelling.rename('upwelling flux')

'''
and save the data to file
'''

all_cubes = [flux_cube, flux_average, flux_sst, flux_upwelling, cold_water_volume, H, sst, pressure, windspeed, heat, delta_pCO2, pCO2_air, pCO2_ocean, isotherm_anomaly]
iris.save(all_cubes, 'full_model_full_basin.nc')


