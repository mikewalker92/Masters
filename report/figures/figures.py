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
'''

'''
--------------------------------------------------------------------------------
import the required modules
--------------------------------------------------------------------------------
'''

import iris
import iris.quickplot as qplt
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np

import masters_library as lib
import enso_model 

show1 = False
show2 = False
show3 = False
show4 = False
show5 = False
show6 = False
show7 = False
show8 = False
show9 = True
show10 = False

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

# We also load the data file containing the observed global CO2 flux.

filename = '/home/michael/git/Masters/report/figures/global_flux.nc'
global_flux = iris.load_cube(filename)


'''
--------------------------------------------------------------------------------
We define the parameters used in the model
--------------------------------------------------------------------------------
'''
start_year = lib.start_year

selected_lat = 3
selected_lon = 8
heat_ref = heat[4,2].collapsed('time', iris.analysis.MEAN)

selected_lat2 = 3
selected_lon2 = 3

f = 3.8e-4
A = 1.085e-4
R = 5000.
a = 0.0423
rho = 1000.
c = 4.18e6

pressure_const = 101000

const = {'f':f,
         'A':A,
         'R':R,
         'a':a,
         'pressure_const':pressure_const,
         'heat_ref':heat_ref,
         'rho':rho,
         'c':c}

nino_time = 500
nina_time = 600

nino_date = start_year + nino_time / 12
nina_date = start_year + nina_time / 12


'''
--------------------------------------------------------------------------------
Figure 1: Isotherm depth along the equator.
--------------------------------------------------------------------------------
'''
if show1:

    # We must reduce our 3 dimensional cubes to 1 dimension.
    # We first specify only data along the equator.

    equator_isotherm = isotherm[4]

    # We collapse time by taking the mean, or by taking
    # particular times.

    mean_profile = equator_isotherm.collapsed('time', iris.analysis.MEAN)
    nino_profile = equator_isotherm[:,nino_time]
    nina_profile = equator_isotherm[:,nina_time]

    # We now plot these profiles on the same figure

    qplt.plot(mean_profile, label='Mean profile', color='green')
    qplt.plot(nino_profile, label='Profile during El Nino', color='red')
    qplt.plot(nina_profile, label='Profile during La Nina', color='blue')
    plt.legend()
    plt.title('Isotherm Depth Along the Equator')

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
    plt.title('Scatter Plot of SST Anomaly against Isotherm Anomaly')
    plt.show()

'''
--------------------------------------------------------------------------------
Figure 3: Comparison of model and observed data. 
--------------------------------------------------------------------------------
'''

if show3:

    filename = '/home/michael/git/Masters/report/figures/enso_model.nc'
    model_data = iris.load_cube(filename)

    observed_data = isotherm_anomaly[selected_lat, selected_lon]

    plt.subplot(3,2,1)
    qplt.plot(model_data)

    plt.subplot(3,2,2)
    qplt.plot(observed_data, label='Observed isotherm anomaly')

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
    
    qplt.pcolormesh(global_flux)
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
        
        qplt.pcolormesh(global_flux)
        plt.gca().coastlines()
        plt.title('Observed Time Averaged Carbon Flux')
        plt.xlim(-50, 95)
        plt.ylim(-11, 11)
        
        ax = plt.subplot(212, projection=plate_carree)
        
        qplt.pcolormesh(mean_flux)
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
    
    flux_4s_model = mean_flux[5]
    flux_4s_observed = global_flux[21]
    
    qplt.plot(flux_4s_model, label='Model Flux')
    qplt.plot(flux_4s_observed, label='Observed_flux')
    plt.xlim(130, 250)
    plt.legend()
    
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
    
    qplt.plot(flux_sst_point, label='Carbon Flux due to SST')
    qplt.plot(flux_upwelling_point, label='Carbon Flux due to Upwelling')
    qplt.plot(flux_total_point, label='Total Carbon Flux')
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
    
    qplt.plot(flux_west, label='Carbon Flux in West of Basin')
    qplt.plot(flux_east, label='Carbon Flux in East of Basin')
    plt.legend()
    plt.show()
    
'''
--------------------------------------------------------------------------------
Figure 9: Flux all variables vs Flux just isotherm depth
--------------------------------------------------------------------------------
'''

if show9 or show10:
    
    data = [isotherm_anomaly, 
            sst_anomaly, 
            heat_anomaly, 
            pressure_anomaly,
            wind_anomaly]
    
    correlations = get_correlations(data)
    
    iso_data = isotherm_anomaly[selected_lat, selected_lon]
    
    correlation_data = []
    for cube in correlations:
        correlation_data.append(cube[selected_lat, selected_lon])
    
    if show9:
    
        flux_cubes = lib.calculate_flux_iso_data(iso_data, correlation_data, const)
        
        flux_iso = flux_cubes[0]
        
        flux_total = predictions[0]
        flux_total_point = flux_total[selected_lat, selected_lon]
        
        qplt.plot(flux_iso, label='Flux based on Isotherm Depth')
        qplt.plot(flux_total_point, label='Flux based on all variables')
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
    
    flux_cubes = lib.caclulate_flux_iso_data(model_output, correlation_data, const)
    
    flux_total = flux_cubes[0]
    flux_sst = flux_cubes[1]
    flux_upwelling = flux_cubes[2]
    
    qplt.plot(flux_total, label='Total Carbon Flux')
    qplt.plot(flux_sst, label='Carbon Flux due to SST')
    qplt.plot(flux_upwelling, label='Carbon Flux due to Upwelling')
    plt.legend()
    plt.show()





