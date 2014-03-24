import iris

import sys
sys.path.append('/home/michael/Desktop/git/Masters/lib')
import lib

'''
In the following scrip, we calculate the carbon fluxes from this equation:

Carbon Flux = solubility * gas_transfer_velocity * Henrys_constant* [(partial pressure of disolved CO2) - (partial pressure of atmospheric CO2)]

This calculation only accounts for the carbon flux due to the change in surface 
temperature of the water.

ASSUMPTIONS
------------------------------------------------------------------------

constant mole fraction of CO2
Assume that Henrys Constant, H = 3.47 e-4, where concentration = H * pressure 


PARTIAL PRESSURE AIR
------------------------------------------------------------------------

    for an ideal gas, we have that pressure is directly to temperature. 
    
    we therefore have that pCO2_air = f*p = B*f*T,
    
    where p is the atmosheric pressure, and f is the mole fraction of 
    co2 in the atmosphere


PARTIAL PRESSURE OCEAN
------------------------------------------------------------------------

    d(pCO2)/dT = a*(pCO2)
    
    which gives (pCO2) = A * exp(a*T)
    
    We will take a = 0.0423, 
    and assume that zero flux occurs at 299.6K;
    A = 0.000123
    
    
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
    
    CO2_flux = S*k*H * (A*exp(a*T) - f*p)
    
'''
    
air_temp = iris.load_cube('/home/michael/Scitools/iris-sample-data/sample_data/air_temp.pp')
pressure = iris.load_cube('/home/michael/Desktop/git/Masters/pressure/pressure.nc')
pressure = pressure * 100
pressure.units = 'Pa'
wind = iris.load_cube('/home/michael/Desktop/git/Masters/wind/windspeed.nc')
SST_cubes = iris.load('/home/michael/Desktop/git/Masters/SST_daily/ersst.201201.nc')
SST = SST_cubes[0]
SST = SST[0,0]
SST.convert_units('kelvin')

air_temp = lib.make_same_grid(air_temp, SST)
pressure = lib.make_same_grid(pressure, SST)
wind = lib.make_same_grid(wind, SST)

S = -1*(0.07*SST - 22.4) * (1000.0/44.0)
S.rename('S')
k = 87.6 * (lib.force_maths('subtract', 0.31*wind**2, 0.91*wind) + 7.76)
k.rename('k')
a = 0.0423
pCO2_ocean = 1.283e-3 * iris.analysis.maths.exp(a*SST)
pCO2_ocean.rename('pCO2_ocean')
pCO2_air = 395e-6 * pressure
pCO2_air.rename('pCO2_air')

Sk = lib.force_maths('multiply', S, k)
Sk.rename('Sk')
delta_pCO2 = lib.force_maths('subtract', pCO2_ocean, pCO2_air)
delta_pCO2.rename('delta_pCO2')

carbon_flux = lib.force_maths('multiply', Sk, delta_pCO2) / pCO2_air
carbon_flux.rename('carbon flux due to heat')

all_cubes = [S, k, pCO2_air, pCO2_ocean, carbon_flux, Sk, delta_pCO2]
iris.save(all_cubes, 'carbon flux due to heat.nc')








