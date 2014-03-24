"""
This script is a re-write of the script written by Eli Galanti based
on the simple model detailed in the paper;

El Nino Chaos: Overlapping of Resonances Between the Seasonal Cycle and the
Pacific Ocean-Atmospheric Oscillator. 
Eli Tziperman, Lewi Stone, Mark A. Cane, Hans Jarosh

Based on code written by Eli Galanti

In the following code, we will be looking to solve the following equation;

dh(t)/dt = a*A(h{t - [L/(2Ck)]}) - b*A(h{t - [L/Ck + L/2Cr]}) + c*cos(w*t)

where we have defined that;

h is the deviation in thermocline depth from seasonal values at the eastern
boundary

t is time

L is the basin width

w is the annual frequency of the seasonal forcing

Ck and Cr are the speeds of the Kelvin and Rossby waves respectivly.

A(h) relates the wind stress to SST and SST to thermocline depth. 
"""

import matplotlib.pyplot as plt
import numpy as np
import iris
import iris.quickplot as qplt
import iris.plot as iplt
from scipy.fftpack import rfft, fftfreq


# We begin by creating a 1D array h, representing h at each time step.
h = []
AmN1_array = []
AmN2_array = []
seasonal = []

# We give an intial deviation
dt = 1
start_time = int(400/dt)
end_time = int(100000/dt)
for _ in xrange(start_time):
    h.append(1.0e-4)
    AmN1_array.append(0)
    AmN2_array.append(0)
    seasonal.append(0)
for _ in xrange(end_time - start_time):
    h.append(0.0)


# We now construct a hyperbolic tangent function to smooth out the step function
kappa = 2.0
a_plus = 1.
a_minus = 1.
b_plus = 1.51
b_minus = - b_plus / 5.
h_plus = (b_plus / (kappa*a_plus)) * (a_plus - 1)
h_minus = (b_minus / (kappa*a_minus)) * (a_minus - 1)


# parameters for the delayed equation
month = 30.
w = 2.0*np.pi/(12.0*month)
a = 1./180.
b = 1./120.
c = 1./238.

L = 1.
Ck = 1./(2.3*month)
Cr = Ck/3
seasonality_phase_months = 3.0
seasonality_phase = 2.0*np.pi*seasonality_phase_months/12.0

# parameters concerning delay times
tau1 = L/(2*Ck)
N1 = int(tau1 / dt)
tau2 = L/Ck + L/(2*Cr)
N2 = int(tau2 / dt)

# solve the equation
for index in xrange(start_time, end_time):
    # calculate A[h(index - N1)]
    delayed_contribution = h[index - N1]
    if delayed_contribution > h_plus:
        AmN1 = b_plus + (b_plus/a_plus) * (np.tanh((kappa*a_plus/b_plus) * (delayed_contribution - h_plus)) - 1.0)
    elif delayed_contribution <= h_plus and delayed_contribution > h_minus:
        AmN1 = kappa * delayed_contribution
    else:
        AmN1 = b_minus + (b_minus/a_minus) * (np.tanh((kappa * a_minus/b_minus) * (delayed_contribution - h_minus)) - 1.0)

    # calculate A[h(index - N2)]
    delayed_contribution = h[index - N2]
    if delayed_contribution > h_plus:
        AmN2 = b_plus + (b_plus/a_plus) * (np.tanh((kappa*a_plus/b_plus) * (delayed_contribution - h_plus)) -1.0)
    elif delayed_contribution <= h_plus and delayed_contribution > h_minus:
        AmN2 = kappa * delayed_contribution
    else:
        AmN2 = b_minus + (b_minus/a_minus) * (np.tanh((kappa * a_minus/b_minus) * (delayed_contribution - h_minus)) -1.0)

    time_now = dt * index
    # we now propogate h in time. 
    h[index] = h[index - 1] + dt*(a*AmN1 - b*AmN2 + c*np.cos(w*dt*index + seasonality_phase))
    AmN1_array.append((a/b) * AmN1)
    AmN2_array.append((-1)*AmN2)
    seasonal.append((c/b) * np.cos(w*dt*index + seasonality_phase))

time_points = [(index*dt)/360.0 for index in xrange(1, end_time+1)]

time = iris.coords.DimCoord(time_points, long_name='time', units='years')
cube = iris.cube.Cube(h, long_name='kappa = ' + str(kappa) + ', dt = ' + str(dt) + ', b+ = ' + str(b_plus), units='m', dim_coords_and_dims=[(time, 0)])

iris.save(cube, 'enso_model.nc')

plt.plot(h, label='anomaly')
plt.plot(AmN1_array, label='AmN1')
plt.plot(AmN2_array, label='AmN2')
plt.plot(seasonal, label='seasonal')
plt.legend()
plt.grid()
iplt.show()

delay = int(360/dt)
record_start = 40000
record_end = 90000

h_early = [h[index - delay] for index in xrange(record_start, record_end)]
signal = np.array(h_early)
h_late = [h[index] for index in xrange(record_start, record_end)]

fft = np.abs(rfft(signal))**2

rate = 180./dt
x = [index*rate/len(signal) for index in xrange(len(signal))]
x = np.array(x)

plt.plot(x, fft)
plt.xlim(0,1.5)
plt.show()

plt.scatter(h_early, h_late)
plt.show()
