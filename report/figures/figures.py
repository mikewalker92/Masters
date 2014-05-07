'''
In this script, we can set the parameters used in the project, and create all 
of the plots.

Figures created are as follows:

1. Isotherm depth along the equator.
2. correlation SST to isotherm
3. Comparison of model thermocline and historic
4. Observed global carbon flux
5. Zoomed observed flux vs model flux.
6. Flux at 4S
7. Flux at grid point
8. Flux East vs West
9. Flux all variables vs just isotherm depth
10. flux from ENSO model
11. correlation map
12. SST anomaly EL Nino vs La Nina
'''

'''
--------------------------------------------------------------------------------
import the required modules
--------------------------------------------------------------------------------
'''

import iris
import iris.plot as iplt
import iris.quickplot as qplt
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

import masters_library as lib

show1 = False
show2 = False
show3 = False
show4 = False
show5 = False
show6 = False
show7 = False
show8 = False
show9 = False
show10 = False
show11 = True
show12 = True

'''
--------------------------------------------------------------------------------
We load the data files.
--------------------------------------------------------------------------------
'''

file_location = '/home/michael/git/Masters/report/figures/masters_data.nc'

# First we load the monthly time series for the variables.
isotherm = iris.load(file_location)[6]
sst = iris.load(file_location)[2]
heat = iris.load(file_location)[5]
pressure = iris.load(file_location)[8]
wind = iris.load(file_location)[13]

# We now load the anomaly time series.
isotherm_anomaly = iris.load(file_location)[14]
sst_anomaly = iris.load(file_location)[1]
heat_anomaly = iris.load(file_location)[12]
pressure_anomaly = iris.load(file_location)[10]
wind_anomaly = iris.load(file_location)[7]

# And now the means for each month of the year.
means_sst = iris.load(file_location)[4]
means_heat = iris.load(file_location)[3]
means_pressure = iris.load(file_location)[0]
means_wind = iris.load(file_location)[11]

# We also load the data file containing the observed global CO2 flux.

filename = '/home/michael/git/Masters/report/figures/global_flux.nc'
global_flux = iris.load_cube(filename)    
global_flux.units = 'mol m-2 yr-1'


'''
--------------------------------------------------------------------------------
We define the parameters used in the model
--------------------------------------------------------------------------------
'''
start_year = lib.start_year

selected_lat = 3
selected_lon = 8
heat_ref = heat[2,2].collapsed('time', iris.analysis.MEAN)

selected_lat2 = 3
selected_lon2 = 3

f = 3.8e-4
A = 1.085e-4
R = 5000.
a = 0.0423
rho = 1000.
c = 4.18e6
scale_factor = 80

pressure_const = 101000

const = {'f':f,
         'A':A,
         'R':R,
         'a':a,
         'pressure_const':pressure_const,
         'heat_ref':heat_ref,
         'rho':rho,
         'c':c,
         'selected_lat' : selected_lat,
         'selected_lon' : selected_lon,
         'scale_factor' : scale_factor}

nino_time = 456
nina_time = 469


'''
--------------------------------------------------------------------------------
Figure 1: Isotherm depth along the equator.
--------------------------------------------------------------------------------
'''
if show1:

    # We must reduce our 3 dimensional cubes to 1 dimension.
    # We first specify only data along the equator.

    equator_isotherm = isotherm[3]

    # We collapse time by taking the mean, or by taking
    # particular times.

    mean_profile = equator_isotherm.collapsed('time', iris.analysis.MEAN)
    nino_profile = equator_isotherm[:,nino_time]
    nina_profile = equator_isotherm[:,nina_time]

    # We now plot these profiles on the same figure

    qplt.plot(mean_profile, label='Normal Conditions', color='green')
    qplt.plot(nino_profile, label='Profile during El Nino', color='red')
    qplt.plot(nina_profile, label='Profile during La Nina', color='blue')
    plt.legend(loc='upper left')
    plt.ylabel('Isotherm Depth / m')
    plt.title('Isotherm Depth Along the Equator')
    plt.gca().invert_yaxis()

    plt.show()

'''
--------------------------------------------------------------------------------
Figure 2: Correlation of SST anomaly to isotherm anomaly.
--------------------------------------------------------------------------------
'''

if show2:

    # We first collapse the cubes to contain the data for a single gridpoint.

    isotherm_anomaly_at_point = isotherm_anomaly[selected_lat, selected_lon]
    sst_anomaly_at_point = sst_anomaly[selected_lat, selected_lon]

    qplt.scatter(isotherm_anomaly_at_point, sst_anomaly_at_point)
    plt.title('Scatter Plot of SST Anomaly against Isotherm Depth Anomaly')
    plt.show()

'''
--------------------------------------------------------------------------------
Figure 3: Comparison of model and observed data. 
--------------------------------------------------------------------------------
'''

if show3:

    filename = '/home/michael/git/Masters/report/figures/enso_model.nc'
    model_cube = iris.load_cube(filename)
    model_cube = model_cube * scale_factor
    model_data = model_cube.data
    plot_start = 75000
    plot_end = 86000

    observed_data = isotherm_anomaly[selected_lat, selected_lon]

    plt.subplot(2,1,1)
    year = [point/360. + plot_start/360. for point in xrange(len(model_data[plot_start:plot_end]))]
    plt.plot(year, model_data[plot_start:plot_end])
    plt.ylabel('Thermocline Depth Anomaly / m')
    plt.xlabel('Time Since Model Start / years')
    plt.title('Modelled Anomaly in Thermocline Depth')

    plt.subplot(2,1,2)
    year = [start_year + point/12. for point in xrange(len(observed_data.data))]
    plt.plot(year, observed_data.data)
    plt.title('Observed Anomaly in 20C Isotherm Depth')
    plt.xlabel('Time / Years')
    plt.ylabel('20C Isotherm Depth Anomaly / m')
   
    plt.show()
    


'''
--------------------------------------------------------------------------------
Figure 4: Observed Global Carbon flux
--------------------------------------------------------------------------------
'''

if show4:

    # We create the pcolormesh plot
    
    plate_carree = ccrs.PlateCarree(central_longitude = 180)
    ax = plt.axes(projection=plate_carree)
    
    qplt.pcolormesh(global_flux, vmin=-5, vmax=5)
    plt.gca().coastlines()
    plt.title('Observed Time Averaged Carbon Flux')
    
    # We now mark on the box where our data is taken from. 
    
    x, y = [-50, 95, 95, -50, -50], [11, 11, -11, -11, 11]
    
    plt.gca().plot(x, y, transform=plate_carree, color='black')
    
    plt.show()

'''
--------------------------------------------------------------------------------
Figure 5: Zoomed carbon flux vs model carbon flux
--------------------------------------------------------------------------------
'''

if show5 or show6 or show7 or show8 or show9:
    
    # We calculate our prediction of the carbon flux based on the relevant 
    # model.
    
    data = [sst, heat, wind]   
    predictions = lib.calculate_flux_full_data(data, const)
    
    mean_flux = predictions[0].collapsed('time', iris.analysis.MEAN)
    
    if show5:
        
        # We now plot this data against the observed flux in this region. 
        
        plate_carree = ccrs.PlateCarree(central_longitude = 180)
        
        ax = plt.subplot(211, projection=plate_carree)
        
        iplt.pcolormesh(global_flux, vmin=-5, vmax=5)
        plt.gca().coastlines()
        plt.title('Observed Time Averaged Carbon Flux')
        plt.xlim(-50, 95)
        plt.ylim(-11, 11)
        
        ax = plt.subplot(212, projection=plate_carree)
        
        mean_flux.units='mol m-2 yr-1'
        qplt.pcolormesh(mean_flux, vmin=-5, vmax=5)
        plt.gca().coastlines()
        plt.title('Model Time Averaged Carbon Flux')
        plt.xlim(-50, 95)
        plt.ylim(-11, 11)
        
        plt.show()

'''
--------------------------------------------------------------------------------
Figure 6:
--------------------------------------------------------------------------------
'''
if show6:
    
    # We now collapse this cube to show its value at around 4S.
    
    flux_4s_model = mean_flux[3]
    flux_4s_observed = global_flux[21]
    
    qplt.plot(flux_4s_model, label='Modelled Carbon Flux')
    qplt.plot(flux_4s_observed, label='Observed Carbon Flux')
    plt.xlim(147, 265)
    plt.ylabel('Carbon Flux / mol m-2 yr-1')
    plt.title('Flux of Carbon at 2 Degrees South')
    plt.legend(loc='upper left')
    
    plt.show()
    
    
'''
--------------------------------------------------------------------------------
Figure 7: Flux at an individual grid point
--------------------------------------------------------------------------------
'''

if show7:
    
    flux_sst = predictions[1]
    flux_upwelling = predictions[2]
    flux_total = predictions[0]
    
    flux_sst_point = flux_sst[selected_lat, selected_lon]
    flux_upwelling_point = flux_upwelling[selected_lat, selected_lon]
    flux_total_point = flux_total[selected_lat, selected_lon]
    
    time = [start_year + point/12. for point in xrange(len(flux_total_point.data))]
    plt.plot(time, flux_sst_point.data, label='Carbon Flux due to SST')
    plt.plot(time, flux_upwelling_point.data, label='Carbon Flux due to Upwelling')
    plt.plot(time, flux_total_point.data, label='Total Carbon Flux')
    plt.title('Modelled Carbon Flux Time Series')
    plt.xlabel('Time / years')
    plt.ylabel('Carbon Flux / mol m-2 yr-1')
    plt.legend()
    plt.show()

'''
--------------------------------------------------------------------------------
Figure 8: Flux East vs West
--------------------------------------------------------------------------------
'''

if show8:
    
    flux_total = predictions[0]
    
    flux_west = flux_total[selected_lat2, selected_lon2]
    flux_east = flux_total[selected_lat, selected_lon]
    
    time = [start_year + point/12. for point in xrange(len(flux_west.data))]
    
    plt.plot(time, flux_west.data, label='Carbon Flux in West of Basin')
    plt.plot(time, flux_east.data, label='Carbon Flux in East of Basin')
    plt.title('Comparison of Carbon Flux in East and West Eqautorial Pacific')
    plt.xlabel('year')
    plt.ylabel('Carbon Flux / mol m-2 yr-1')
    plt.legend()
    plt.show()
    
'''
--------------------------------------------------------------------------------
Figure 9: Flux all variables vs Flux just isotherm depth
--------------------------------------------------------------------------------
'''

if show9 or show10 or show11:
    
    sst_correlations = lib.get_correlations(isotherm_anomaly, sst_anomaly)
    heat_correlations = lib.get_correlations(isotherm_anomaly, heat_anomaly)
    pressure_correlations = lib.get_correlations(isotherm_anomaly, pressure_anomaly)
    wind_correlations = lib.get_correlations(isotherm_anomaly, wind_anomaly)
    
    iso_data = isotherm_anomaly[selected_lat, selected_lon]
    
    correlation_data = {'gradient_sst' : sst_correlations[1][selected_lat, selected_lon],
                        'gradient_heat' : heat_correlations[1][selected_lat, selected_lon],
                        'gradient_pressure' : pressure_correlations[1][selected_lat, selected_lon],
                        'gradient_wind' : wind_correlations[1][selected_lat, selected_lon],
                        'means_sst' : means_sst[selected_lat, selected_lon],
                        'means_heat' : means_heat[selected_lat, selected_lon],
                        'means_pressure' : means_pressure[selected_lat, selected_lon],
                        'means_wind' : means_wind[selected_lat, selected_lon]}
    
    if show9:
    
        flux_cubes = lib.calculate_flux_iso_data(iso_data, correlation_data, const)
        
        flux_iso = flux_cubes[0]
        
        flux_total = predictions[0]
        flux_total_point = flux_total[selected_lat, selected_lon]
        
        time = [start_year + point/12. for point in xrange(len(flux_total_point.data))]
        plt.plot(time, flux_iso.data, label='Flux based on Isotherm Depth')
        plt.plot(time, flux_total_point.data, label='Flux based on all variables')
        plt.title('Comparison of Methods of Estimating Carbon Flux')
        plt.xlabel('year')
        plt.ylabel('Carbon Flux / mol m-2 yr-1')
        plt.legend()
        plt.show()

'''
--------------------------------------------------------------------------------
Figure 10: Flux from ENSO model.
--------------------------------------------------------------------------------
'''

if show10:

    filename = '/home/michael/git/Masters/report/figures/enso_model.nc'
    model_output = iris.load_cube(filename)
    model_output = model_output * scale_factor
    
    model_output = model_output[75000:86000]

    flux_cubes = lib.calculate_flux_iso_model(model_output, correlation_data, const)
    
    flux_total = flux_cubes[0]
    flux_sst = flux_cubes[1]
    flux_upwelling = flux_cubes[2]
    
    qplt.plot(flux_total, label='Total Carbon Flux')
    qplt.plot(flux_sst, label='Carbon Flux due to SST')
    qplt.plot(flux_upwelling, label='Carbon Flux due to Upwelling')
    plt.title('Carbon Flux Based on Model of Thermocline Depth Anomaly')
    plt.xlabel('Time since model start / years')
    plt.ylabel('Carbon Flux / mol m-2 yr-1')
    plt.legend()
    plt.show()


'''
--------------------------------------------------------------------------------
Figure 11: SST correlation across the basin
--------------------------------------------------------------------------------
'''

if show11:
    
    pmcc = sst_correlations[0]
    
    cube = sst_anomaly[:,:,0]
    cube.data = pmcc.data
    cube.units = None
    
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
    
    qplt.pcolormesh(cube,cmap='brewer_Reds_09', vmax=1, vmin=0)
    plt.title('PMCC between SST Anomaly and Isotherm Depth Anomaly')
    ax.coastlines()
    # Add a citation to the plot.
    iplt.citation(iris.plot.BREWER_CITE)
    
    plt.show()

'''
--------------------------------------------------------------------------------
Figure 12: SST anomaly El Nino vs La Nina
--------------------------------------------------------------------------------
'''

if show12:
    
    el_nino = sst_anomaly[:,:,nino_time]
    la_nina = sst_anomaly[:,:,nina_time]
    
    plate_carree = ccrs.PlateCarree(central_longitude = 180)
    
    plt.subplot(211, projection=plate_carree)
    
    iplt.pcolormesh(el_nino, vmin = -4, vmax = 4)
    plt.title('SST Anomaly during an El Nino Event')
    plt.gca().coastlines()

    
    plt.subplot(212, projection=plate_carree)
    
    qplt.pcolormesh(la_nina, vmin = -4, vmax = 4)
    plt.title('SST Anomaly during a La Nina Event')
    plt.gca().coastlines()
    
    plt.show()
   
    
