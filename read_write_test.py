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
from read_write import *

READ_MODE = 1
WRITE_MODE = 2

# Define file names as strings here
# ifile = "sin_wave.pak52"
ifile = "output.bin"
ofile = "should_match_ifile.bin"

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
        in_data_set = py_read_one_data_set(df_i)
        py_write_one_data_set(df_o, in_data_set)

        # be sure to free memory after use
        py_free_bin_pak_data(in_data_set) 
        
        py_close_pak_bin_file(df_i)
        py_close_pak_bin_file(df_o)

if __name__ == "__main__":
    unittest.main()
