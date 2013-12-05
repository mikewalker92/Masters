import iris
import iris.analysis.maths as maths

'''
In this script, we aim to calculate the value of the heat content which we would
expect to see without upwelling. In this case, we have opted for the most simple
possible model, taking the temperature of the upper model to be T0 and the temperature
of the deep layer to be Td. We then take that the heat per unit volume is proportional 
to the temperature, and use the following equation:

Expected Heat Content = A * (T0 * thermocline_depth + Td * (300 - thermocline_depth))

Where A is a constant of proportionality, calculated by assuming no upwelling in the 
west of the basin. 

'''

A = 0.005
T0 = 29
Td = 15

thermocline_depth = iris.load('/home/michael/Desktop/20C/20C_cubes.nc')[0]

upper_level = maths.multiply(thermocline_depth, T0)
layer_depth = maths.subtract(thermocline_depth, 300)
layer_depth = maths.multiply(layer_depth, -1)
lower_level = maths.multiply(layer_depth, Td)

unscaled_heat = maths.add(upper_level, lower_level)
expected_heat = maths.multiply(unscaled_heat, A)

expected_heat.units = 'J'

iris.save(expected_heat, 'expected_heat.nc')

