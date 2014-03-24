import numpy as np
from scipy.fftpack import rfft, fftfreq
import matplotlib.pyplot as plt

time_step = 10./2000.
time   = np.linspace(0,10,2000)
signal = np.cos(5*np.pi*time)

W = [index*time_step/len(time) for index in xrange(len(time))]
f_signal = np.abs(rfft(signal))**2

rate = 1./time_step
x = [index*rate/len(signal) for index in xrange(len(signal))]
x = np.array(x)

plt.subplot(121)
plt.plot(time, signal)
plt.subplot(122)
plt.plot(x, (f_signal))
plt.show()