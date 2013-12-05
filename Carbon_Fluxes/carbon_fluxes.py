import iris

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

Taking zero flux at 300K gives A = 0.000109

'''

temperature = iris.load_cube('/home/michael/Desktop/SST_daily/SST_raw.nc')
windspeed = iris.load('/home/michael/Desktop/Wspd_daily/Wspd.nc')[0]

carbon_flux = (windspeed**2) * (0.000109 * iris.analysis.maths.exp(0.0423 * temperature) - 35.5)

mean_carbon_flux = carbon_flux.collapsed('time', iris.analysis.MEAN)

all_cubes = (carbon_flux, mean_carbon_flux)

iris.save(all_cubes, 'carbon_flux.nc')
