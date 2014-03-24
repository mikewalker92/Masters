import iris

isotherm = iris.load('/home/michael/Desktop/git/Masters/trends/20isotherm/isotherm_cubes.nc')[2]
isotherm = isotherm[3,9]

sst_mean = iris.load('/home/michael/Desktop/git/Masters/trends/sst/sst_cubes.nc')[0]
windspeed_mean = iris.load('/home/michael/Desktop/git/Masters/trends/windspeed/windspeed_cubes.nc')[4]
pressure_mean = iris.load('/home/michael/Desktop/git/Masters/trends/pressure/pressure_cubes.nc')[1]

sst_mean = sst_mean.data[3,9]
windspeed_mean = windspeed_mean.data[3,9]
pressure_mean = pressure_mean.data[3,9]

sst_grad = 0.05336
sst_intercept = -0.02202

windspeed_grad = 0.02201
windspeed_intercept = 0.02995

pressure_grad = -0.01826
pressure_intercept = -0.03878

sst = isotherm * sst_grad + sst_intercept + sst_mean
sst.units = None
windspeed = isotherm * windspeed_grad + windspeed_intercept + windspeed_mean
windspeed.units = None
pressure = isotherm * pressure_grad + pressure_intercept + pressure_mean
pressure.units = None

S = -1*(0.07*sst - 22.4) * (1000./44.0)
S.rename('S')
k = 87.6 * (0.31*windspeed**2 - 0.91*windspeed) + 7.76
k.rename('k')
a = 0.0423
pCO2_ocean = 1.283e-3 * iris.analysis.maths.exp(a*sst)
pCO2_ocean.rename('pCO2_ocean')
pCO2_ocean.units = None
pCO2_air = 395e-6 * pressure
pCO2_air.rename('pCO2_air')

Sk =  S * k
delta_pCO2 = pCO2_ocean - pCO2_air

carbon_flux = Sk * delta_pCO2 / pCO2_air
carbon_flux.rename('carbon flux due to heat')

all_cubes = [S, k, pCO2_ocean, pCO2_air, carbon_flux]

iris.save(all_cubes, 'prediction_from_data_heat_only.nc')
