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
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import rfft, fftfreq

'''
We first load the El Nino parameter. In this case we will use the 20 degree
isotherm depth anomaly as an analog for the strength of El Nino.
'''
isotherm_anomaly = iris.load('/home/michael/Desktop/git/Masters/trends/20isotherm/isotherm_cubes.nc')[5][3,9]
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
pressure_mean_cube = iris.load('/home/michael/Desktop/git/Masters/trends/pressure/pressure_cubes.nc')[1]
windspeed_mean_cube = iris.load('/home/michael/Desktop/git/Masters/trends/windspeed/windspeed_cubes.nc')[4]
heat_mean_cube = iris.load('/home/michael/Desktop/git/Masters/trends/heat/heat_cubes.nc')[4]

sst_gradient_cube = iris.load('/home/michael/Desktop/git/Masters/trends/sst/pmcc.nc')[2]
pressure_gradient_cube = iris.load('/home/michael/Desktop/git/Masters/trends/pressure/pmcc.nc')[2]
windspeed_gradient_cube = iris.load('/home/michael/Desktop/git/Masters/trends/windspeed/pmcc.nc')[2]
heat_gradient_cube = iris.load('/home/michael/Desktop/git/Masters/trends/heat/pmcc.nc')[2]

sst_mean = sst_mean_cube.data[3,9]
pressure_mean = pressure_mean_cube.data[3,9]
windspeed_mean = windspeed_mean_cube.data[3,9]
heat_mean = heat_mean_cube.data[3,9]

sst_gradient = sst_gradient_cube.data[3,9]
pressure_gradient = pressure_gradient_cube.data[3,9]
windspeed_gradient = windspeed_gradient_cube.data[3,9]
heat_gradient = heat_gradient_cube.data[3,9]

'''
We are now able to construct our aproximate variables based on the isotherm 
anomaly.
'''
sst = sst_mean + sst_gradient*isotherm_anomaly
pressure = (pressure_mean + pressure_gradient*isotherm_anomaly) * 100
windspeed = windspeed_mean + windspeed_gradient*isotherm_anomaly
heat = (heat_mean + heat_gradient*isotherm_anomaly) *10.**10.

sst.units=None
pressure.units=None
windspeed.units=None
heat.units=None

sst.rename('sst')
pressure.rename('pressure')
windspeed.rename('windspeed')
heat.rename('heat')


'''
We now define some parameters of the model
'''

A = 1.283e-4
R = 10.
f = 380e-6
delta_T = 5
expected_heat = heat_mean_cube.data[3,2]
time_step = 1./12.

'''
and some constants
'''
a = 0.0423
specific_heat = 4.18e6
water_density = 1000.


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

missing_heat = heat - expected_heat
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
flux.rename('total flux')

delay = 12

flux_later = flux.data[delay:]
flux_earlier = []
for index, point in enumerate(flux.data):
    if index < len(flux_later):
        flux_earlier.append(point)

plt.plot(flux.data)
plt.show()

signal = flux.data

fft = np.abs(rfft(signal))**2

rate = 6.
x = [index*rate/len(signal) for index in xrange(len(signal))]
x = np.array(x)

plt.plot(x, fft)
plt.xlim(0,2)
plt.show()

plt.scatter(flux_later, flux_earlier)
plt.show()

'''
and save the data to file
'''

all_cubes = [flux, flux_sst, flux_upwelling, cold_water_volume, H, sst, pressure, windspeed, heat, 
             delta_pCO2, pCO2_air, pCO2_ocean, isotherm_anomaly]
iris.save(all_cubes, 'full_model.nc')


