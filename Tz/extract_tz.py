import numpy as np
import iris
import sys
sys.path.append('/home/michael/Desktop/git/Masters/lib')
import lib

Tz_file = open('/home/michael/Desktop/git/Masters/Tz/t0n140w_mon.ascii')

all_depths = {'d1' : [],
              'd3' : [],
              'd5' : [],
              'd10' : [],
              'd13' : [],
              'd20' : [],
              'd25' : [],
              'd28' : [],
              'd35' : [],
              'd40' : [],
              'd45' : [],
              'd48' : [],
              'd60' : [],
              'd80' : [],
              'd83' : [],
              'd100' : [],
              'd120' : [],
              'd123' : [],
              'd140' : [],
              'd160' : [],
              'd180' : [],
              'd200' : [],
              'd250' : [],
              'd300' : [],
              'd500' : []}

lines_to_ignore = (' Location', ' Units', ' Time', ' Index', ' YYYY')

depths = []
for line in Tz_file:
    if line.startswith(lines_to_ignore):
        continue
    
    elif line.startswith(' Depth'):
        depths = lib.convert_to_csv(line)
        depths = depths.split(',')
    
    else:
        values = lib.convert_to_csv(line)
        values = values.split(',')
        for counter in xrange(len(values)):
            if counter == 0 or counter == 1 or counter == len(values)-1:
                pass
            else:
                if values[counter] != '-9.999':
                    depth_name = 'd' + str(depths[counter-1])
                    all_depths[depth_name].append(float(values[counter]))

depth_list = ['d1','d3','d5','d10','d13','d20','d25','d28','d35','d40','d45',
              'd48','d60','d80','d83','d100','d120','d123','d140','d160', 'd180',
              'd200','d250','d300','d500']

data = []           
for depth in depth_list:
    data.append(sum(all_depths[depth]) / len(all_depths[depth]))
    
depth_points = [1,3,5,10,13,20,25,28,35,40,45,48,60,80,83,100,
                120,123,140,160,180,200,250,300,500]
depth = iris.coords.DimCoord(depth_points, standard_name = 'depth', units = 'm')

Tz = iris.cube.Cube(data, long_name='Tz at 0n 140W', units='C', dim_coords_and_dims=[(depth, 0)])

iris.save(Tz, 'Tz.nc')
        
        
        
    