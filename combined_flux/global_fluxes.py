import iris
import numpy as np
import sys
sys.path.append('/home/michael/Desktop/git/Masters/lib')
import lib

redo_regrid = False

upwelling = iris.load_cube('/home/michael/Desktop/git/Masters/upwelling/upwelling.nc')

a = 0
b = 1

averaged_upwelling = upwelling[a:(b+1)]
averaged_upwelling = averaged_upwelling.collapsed('depth', iris.analysis.MEAN)

depth = upwelling.coord('depth').points
name = 'averaged upwelling from ' + str(depth[a]) + ' to ' + str(depth[b])
averaged_upwelling.rename(name)

if redo_regrid:
    heat_flux = iris.load('/home/michael/Desktop/git/Masters/heat_flux/heat_flux.nc')[1]
    heat_flux = lib.make_same_grid(heat_flux, averaged_upwelling)
    truth = iris.load_cube('/home/michael/Desktop/git/Masters/combined_flux/true_flux.nc')
    truth = lib.make_same_grid(truth, averaged_upwelling)
    iris.save(heat_flux, 'regridded_heat_flux.nc')
    iris.save(truth, 'regridded_truth.nc')
else:
    heat_flux = iris.load_cube('/home/michael/Desktop/git/Masters/combined_flux/regridded_heat_flux.nc')
    truth = iris.load_cube('/home/michael/Desktop/git/Masters/combined_flux/regridded_truth.nc')

heat_flux_scaling = 40
upwelling_scaling = 1

dT = 1.0/6.0

flux_at_each_depth = (upwelling / upwelling_scaling) * 501709 * dT
flux_at_each_depth.rename('flux for given depth')

flux_due_to_heat = (heat_flux / heat_flux_scaling) - 0.5
flux_due_to_heat.rename('flux due to heat')
flux_due_to_upwelling = (averaged_upwelling / upwelling_scaling) * 501709 * dT
flux_due_to_upwelling.rename('flux_due_to_upwelling') 

flux_due_to_upwelling.remove_coord('depth')
flux_due_to_heat.remove_coord('year')


total = lib.force_maths('add', flux_due_to_upwelling, flux_due_to_heat)
total.rename('total flux')

error = lib.force_maths('subtract', total, truth)
error.rename('error = (total - truth)')

all_cubes = [heat_flux, averaged_upwelling, flux_due_to_heat, flux_due_to_upwelling, total, error, truth, upwelling, flux_at_each_depth]

iris.save(all_cubes, 'global_total_flux.nc')
