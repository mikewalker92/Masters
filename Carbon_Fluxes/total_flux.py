import iris
import iris.experimental.regrid as regrid
import numpy as np

scale_factor = 50

flux_w = iris.load('/home/michael/Desktop/git/Masters/upflow/CO2_flux_from_upwelling.nc')[1]
flux_w = flux_w / scale_factor
flux_w.units = None
flux_w.rename('flux due to upwelling')
flux_t = iris.load('/home/michael/Desktop/git/Masters/Carbon_Fluxes/CO2_flux_SST.nc')[0]
flux_t = flux_t[0]
flux_t.units = None
regridded_w = iris.load('/home/michael/Desktop/git/Masters/upflow/regridded.nc')[2]
regridded_w = (regridded_w / scale_factor) * 5017091
regridded_w.rename('regridded_w')

regridded_w_masked = iris.load('/home/michael/Desktop/git/Masters/upflow/regridded_masked.nc')[2]
regridded_w_masked = (regridded_w_masked / scale_factor) * 5017091
regridded_w_masked.rename('regridded_w_masked')

new_cs = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)

regridded_t = flux_t
regridded_t.coord('latitude').coord_system = new_cs
regridded_t.coord('longitude').coord_system = new_cs
regridded_t.rename('regridded_t')

regridded_t = regrid.regrid_bilinear_rectilinear_src_and_grid(regridded_t, regridded_w)

flux_t.rename('flux due to temp')

regridded_total = regridded_t + regridded_w
regridded_total.rename('regridded_total')

regridded_masked_total = regridded_t + regridded_w_masked
regridded_masked_total.rename('regridded_masked_total')

lat_points = flux_w.coord('latitude').points
lon_points = flux_w.coord('longitude').points

sample_points = [('latitude', lat_points), ('longitude', lon_points)]

interpolared_t = iris.analysis.interpolate.linear(flux_t, sample_points)

latitude_w = flux_w.coord('latitude')
longitude_w = flux_w.coord('longitude')
latitude_t = interpolared_t.coord('latitude')
longitude_t = interpolared_t.coord('longitude')

flux_w.remove_coord(latitude_w)
flux_w.remove_coord(longitude_w)
interpolared_t.remove_coord(latitude_t)
interpolared_t.remove_coord(longitude_t)

total_flux = flux_w + interpolared_t

flux_w.add_dim_coord(latitude_w, 0)
flux_w.add_dim_coord(longitude_w, 1)
interpolared_t.add_dim_coord(latitude_t, 0)
interpolared_t.add_dim_coord(longitude_t, 1)

total_flux.add_dim_coord(latitude_w, 0)
total_flux.add_dim_coord(longitude_w, 1)
total_flux.rename('total flux')

all_cubes = [total_flux, flux_w, interpolared_t, regridded_w, regridded_t,  regridded_total, regridded_w_masked, regridded_masked_total]

iris.save(all_cubes, 'carbon_flux_global.nc')
    

            