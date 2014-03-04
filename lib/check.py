import iris

def stuff_1(x):
    y = x + 1
    return y

def stuff_2(x):
    y = x + 0
    y.remove_coord('latitude')
    return y

data = [(2,3,4),(5,6,7),(8,9,0)]

latitude = iris.coords.DimCoord([1,2,3], long_name = 'latitude')
longitude = iris.coords.DimCoord([1,2,3], long_name = 'longitude')

cube1 = iris.cube.Cube(data, long_name = 'cube', dim_coords_and_dims = [(latitude, 0), (longitude, 1)])
cube1.rename('cube1')

print cube1
print cube1.data

cube2 = stuff_1(cube1)
cube2.rename('cube2')

print cube1
print cube1.data
print cube2
print cube2.data

cube3 = stuff_2(cube1)
cube3.rename('cube3')

print cube1
print cube1.data
print cube2
print cube2.data
print cube3
print cube3.data
