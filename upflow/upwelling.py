import iris

'''
In this script, we will estimate the global CO2 flux due to upwelling (w). 

The model used here is that of a column of rising water in a 2 layer ocean.
The top layer is warmer than the bottom layer by an amount dT. 
The rate at which water passes into this top layer is the rate of upwelling, w.
When water goes from the bottom layer to the top layer, it must increase in temperature
by an amount dT. 
This will lead to a change in the solubility of the water, and so will give a release of 
CO2. 
We assume that in steady state, all of this released CO2 will be transfered to the atmosphere.


Concerns...
    Assuption that all CO2 is released into the atmosphere
    Is it valid to treat as a colum of rising water given that horizontal velocity is much greater
    than vertical velocity?


This model gives us the following equation;

    CO2_flux_per_unit_area = w * change_in_CO2_concentration.
    
To get the concentration, we simply use the solubility S.

We approximate the solubility in this range of temperature and pressure to be 
a function of temperature only as

    S = (22.4 - 0.07*T) g of CO2 per L of water. (where T here is in K)
    
converting into more convenient units, 

    S = (1000/44) * (22.4 - 0.07*T) mols of CO2 per m^3 of water
    
    
The change in S is therefore,

    0.07 * dT

We therefore have that

    CO2_flux = (70 / 44) * w * dT
    
Finally, we would like CO2_flux in units of mol m-2 yr-1,
and so we need w in units of m yr-1.

w is given to us in units of cm s-1, so we require a factor of 60*60*24*365 / 100

Giving us a final equation of 

    CO2_flux = (70 / 44) * (31536000 / 100) * dT * w
    CO2_flux = 501709 * dT * w

'''

w = iris.load('/home/michael/Desktop/git/Masters/upflow/upwelling.nc')[0]
w.rename('upwelling')

dT = 10.0

CO2_flux = 501709 * dT * w 
CO2_flux.rename('CO2 flux')
CO2_flux.units = 'mol m-2 yr-1'

all_cubes = (CO2_flux, w)

iris.save(all_cubes, 'CO2_flux_from_upwelling.nc')
