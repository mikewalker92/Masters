import iris
import sys

sys.path.append('/home/michael/Desktop/git/Masters/SST_daily')
import make_cube_SST

'''
In the following scrip, we calculate the carbon fluxes from this equation:

Carbon Flux = constant * (windspeed)**2 * [(partial pressure of disolved CO2) - (partial pressure of atmospheric CO2)]


For the purposes of this rough calculation, we have;

ignored the effect of advection
ignored the dependance on solubility as this is assumed to be small
assumed the gas transfer velocity to be proportional to windspeed squared

We shall also;

set constant = 1,
assume the the partial pressure of atmospheric CO2 is constant and equal to 35.5 Pa
we assume the variation in disolved CO2 is due to temperature alone, and follows

d(pCO2)/dT = 0.0423(pCO2)

leading to (pCO2) = A * exp(0.0423*T)

Taking zero flux at 300K gives A = 0.000096

'''

SST_cubes = iris.load('/home/michael/Desktop/git/Masters/SST_daily/ersst.201201.nc')
# Wspd_cubes = iris.load('/home/michael/Desktop/git/Masters/Wspd_daily/Wspd_cubes.nc')

SST = SST_cubes[0]
SST.convert_units('kelvin')
Wind = 5

# Wind.units = None

gas_transfer_velocity = 0.31*Wind**2 - 0.91*Wind + 7.76

carbon_flux = 0.328 * (0.0001 * iris.analysis.maths.exp(0.0423 * SST) - 35.5)
carbon_flux.rename('carbon_flux')
# carbon_flux.units = 'mol m-2 yr-1'

# mean_carbon_flux = carbon_flux.collapsed('time', iris.analysis.MEAN)
# mean_carbon_flux.rename('mean_carbon_flux')

# carbon_flux_anomoly = make_cube_SST.convert_to_anomoly(carbon_flux.data, 0, 0)

all_cubes = (carbon_flux, SST)

iris.save(all_cubes, 'carbon_flux_global.nc')