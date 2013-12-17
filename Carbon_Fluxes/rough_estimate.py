import iris


from_SST = iris.load('/home/michael/Desktop/git/Masters/Carbon_Fluxes/carbon_flux.nc')[1]
from_upwell = iris.load_cube('/home/michael/Desktop/git/Masters/Carbon_Fluxes/volume_cold_water.nc')

from_SST.units = None
from_upwell.units = None

total = 2.25 + from_SST + from_upwell
total.rename('rough_estimate')
total.units = 'mol m-2 yr-1'

iris.save(total, 'rough_estimate.nc')

