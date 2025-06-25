# Author: Zach Philip
# Date: June 2nd, 2025
# Property of Whisper Aero

##################################################################################
# This file is designed to test the DLL, ensuring that all functions are working #
# correctly and that the data can be read and written as expected. Prove this    #
# works by running the test and ensuring ofile matches ifile.                    #  
##################################################################################

import unittest
import sys
import os
import ctypes

# needed so debugger can find read_write.py for imports 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.read_write import *
from src.my_function import *

READ_MODE = 1
WRITE_MODE = 2


# Define file names as strings here
ifile = "supporting_files/sin_wave.pak52"
#ifile = "output.bin"
ofile = "test.bin"

class TestBinPakData(unittest.TestCase):
    def test_populate_data(self):
        n_data_arrays = ctypes.c_short()
        dummy = ctypes.c_short()
        n_data_sets = ctypes.c_long()

        df_i = py_open_pak_bin_file(ifile, ctypes.byref(n_data_arrays), READ_MODE)
        df_o = py_open_pak_bin_file(ofile, ctypes.byref(dummy), WRITE_MODE)
        py_write_pak_bin_file_header(df_o, n_data_arrays)

        py_read_data_set_header(df_i, ctypes.byref(n_data_sets))
        py_write_data_set_header(df_o, n_data_sets)
        in_data_set_ptr = py_read_one_data_set(df_i)

        data = in_data_set_ptr.contents
        print_bin_pak_data(data)
        # Convert to Python and apply filter
        y_array = ydata_to_np_array(data)
        x_array = xdata_to_np_array(data)
        z_array = zdata_to_np_array(data)


        # filtered_ydata = y_array
        # filtered_xdata = x_array
        # filtered_zdata = z_array
        # filtered_ydata = apply_gaussian_filter(y_array)
        # filtered_xdata = apply_gaussian_filter(x_array)
        # filtered_zdata = apply_gaussian_filter(z_array)
        # filtered_ydata = ex_diff(y_array)
        # filtered_xdata = ex_diff(x_array)
        # filtered_ydata = ex_a_range(y_array)
        # filtered_xdata = ex_a_range(x_array)
        filtered_ydata = filter_below_threshold(y_array)
        filtered_xdata = filter_below_threshold(x_array)
        filtered_zdata = filter_below_threshold(z_array)

        # Convert back to binPakData format by creating new BinPakData structure and copying values
        new_filtered_data_ptr = copy_bin_data(data, filtered_xdata, filtered_ydata, filtered_zdata)

        print_bin_pak_data(new_filtered_data_ptr.contents)

        py_write_one_data_set(df_o, new_filtered_data_ptr)

        # be sure to free memory after use
        py_free_bin_pak_data(in_data_set_ptr)
        
        py_close_pak_bin_file(df_i)
        py_close_pak_bin_file(df_o)

if __name__ == "__main__":
    unittest.main()
