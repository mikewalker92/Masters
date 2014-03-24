import iris
import sys
sys.path.append('/home/michael/Desktop/git/Masters/lib')
import lib

u = iris.load('/home/michael/Desktop/git/Masters/wind/uwnd.1999.nc')[0]
u = u[:,0]
u = u.collapsed('time', iris.analysis.MEAN)
v = iris.load('/home/michael/Desktop/git/Masters/wind/vwnd.1999.nc')[1]
v = v[:,0]
v = v.collapsed('time', iris.analysis.MEAN)

u_squared = u**2
v_squared = v**2

windspeed_squared = lib.force_maths('add', u_squared, v_squared)
windspeed = windspeed_squared**0.5

iris.save(windspeed, 'windspeed.nc')
