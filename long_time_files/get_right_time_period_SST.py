import iris

SST = iris.load('/home/michael/Desktop/git/Masters/long_time_files/sst.mnmean.nc')[1]

SST = SST[1128:1921]

iris.save(SST, 'sst.nc')