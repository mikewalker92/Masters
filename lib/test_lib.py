import unittest
import iris

import lib

class LibTests(unittest.TestCase):
    
    def test_make_same_grid_source_larger(self):
        
        filename1 = '/home/michael/Scitools/iris-sample-data/sample_data/air_temp.pp'
        source_cube = iris.load_cube(filename1)
        
        filename2 = '/home/michael/Scitools/iris-sample-data/sample_data/pre-industrial.pp'
        grid_cube = iris.load_cube(filename2)
        
        regridded = lib.make_same_grid(source_cube, grid_cube)
        
        grid_shape = regridded.data.shape
        expected_shape = grid_cube.data.shape
        
        self.assertEqual(grid_shape, expected_shape)
        
    
    def test_make_same_grid_source_smaller(self):
    
        filename1 = '/home/michael/Scitools/iris-sample-data/sample_data/pre-industrial.pp'
        source_cube = iris.load_cube(filename1)
        
        filename2 = '/home/michael/Scitools/iris-sample-data/sample_data/air_temp.pp'
        grid_cube = iris.load_cube(filename2)
        
        regridded = lib.make_same_grid(source_cube, grid_cube)
        
        grid_shape = regridded.data.shape
        expected_shape = grid_cube.data.shape
        
        self.assertEqual(grid_shape, expected_shape)

    
    def test_convert_to_csv(self):
        
        test_string = '   Hello. My name   is Mike!   '
        output = lib.convert_to_csv(test_string)
        expected_output = 'Hello.,My,name,is,Mike!,'
        
        self.assertEqual(output, expected_output)
        
if __name__ == '__main__':
    unittest.main()