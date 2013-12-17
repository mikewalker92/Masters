import iris
import sys


'''
In this script, we will estimate the global CO2 flux due to upwelling (w). 

We start with the following equation

    CO2_flux = w * change in concentration.
    
To get the concentration, we simply use the solubility S.

We approximate the solubility in this range of temperature and pressure to be 
a function of temperature only as

    S = (22.4 - 0.07*T) g of CO2 per L of water. 
    
converting into more convenient units, 

    S = (10000/44) * (22.4 - 0.07*T) mols of CO2 per m^3 of water
    
We therefore have that

    CO2_flux = (700 / 44) * w * dT

'''

w = iris.load('/home/michael/Desktop/git/Masters/upflow/upwelling.nc')[0]
w = iris.analysis.maths.multiply(w, (360*24*60*60 / 100))
w.units = 'm yr-1'
w.rename('upwelling')

dT = 10.0

CO2_flux = (1.59 * dT) * w
CO2_flux.rename('CO2 flux')

all_cubes = (CO2_flux, w)

iris.save(all_cubes, 'CO2 flux from upwelling.nc')
