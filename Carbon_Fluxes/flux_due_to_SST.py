import iris
import sys
import math

sys.path.append('/home/michael/Desktop/git/Masters/SST_daily')
import make_cube_SST

'''
In the following scrip, we calculate the carbon fluxes from this equation:

Carbon Flux = solubility * gas_transfer_velocity * Henrys_constant* [(partial pressure of disolved CO2) - (partial pressure of atmospheric CO2)]

This calculation only accounts for the carbon flux due to the change in surface 
temperature of the water.

ASSUMPTIONS
------------------------------------------------------------------------

Assume the the partial pressure of atmospheric CO2 is constant and equal to 35.5 Pa
Assume that Henrys Constant, H = 3.47 e-4, where concentration = H * pressure 



PARTIAL PRESSURE
------------------------------------------------------------------------

    d(pCO2)/dT = a*(pCO2)

which gives (pCO2) = A * exp(a*T)

We will take a = 0.0423, 
and assume that zero flux occurs at 300K;
    A = 


SOLUBILITY
-----------------------------------------------------------------------

From empirical data, we construct a simple equation to approximate the 
solubility of CO2 in seawater in this temperature range.

    S = (22.4 - 0.07*T) / 1000
    
     

GAS TRANSFER VELOCITY
-----------------------------------------------------------------------

In the following script, we shall take the gas transfer constant to be
dependent on windspeed alone, in accordance with

    k = 0.31*windspeed^2 - 0.91*windspeed + 7.76
    
this gives k in units of cm per hour, we therefore require a factor of 
87.6 to convert into units of m per year.

    k = 87.6 * (0.31*windspeed^2 - 0.91*windspeed + 7.76)
    

-----------------------------------------------------------------------
SUMMARY
-----------------------------------------------------------------------
    
    CO2_flux = S*k*H * (A*exp(a*T) - pCO2_air)
    
'''

SST_cubes = iris.load('/home/michael/Desktop/git/Masters/SST_daily/ersst.201201.nc')
SST = SST_cubes[0]
SST.convert_units('kelvin')

# Define Constants
windspeed = 4
k = 87.6 * (0.31*windspeed**2 - 0.91*windspeed + 7.76)
a = 0.0423
pCO2_air = 35.5
reference_temp = 300
A = pCO2_air / (math.exp(a*reference_temp))
H = 0.000347

# make solubility cube
temp_adjustment = -0.00007 * SST
S = iris.analysis.maths.add(temp_adjustment, 0.0224)
S.rename('Solubility')

pCO2_ocean = A * iris.analysis.maths.exp(a*SST)

CO2_flux = k*H*S*(pCO2_ocean - pCO2_air)
CO2_flux.rename('CO2 flux due to surface temperature')
CO2_flux.units = 'mol m-2 yr-1'

mean_carbon_flux = CO2_flux.collapsed('time', iris.analysis.MEAN)
mean_carbon_flux.rename('mean_carbon_flux')

# carbon_flux_anomoly = make_cube_SST.convert_to_anomoly(carbon_flux.data, 0, 0)

all_cubes = (CO2_flux, mean_carbon_flux, S)

iris.save(all_cubes, 'CO2_flux_SST.nc')