# Author: Zach Philip
# Date: June 2nd, 2025
# Property of Whisper Aero

##################################################################################
# This file is designed to complete the cull cycle of reading in, scaling,       #
# and writing data.                                                              #
# This file asserts that two BinPakData structures match. The first structure is #
# the read from the ifile. This read is written to ofile. The second read is from# 
# the ofile.                                                                     #  
##################################################################################

import unittest
import sys
import os
import ctypes

# Line below needed in some instances depending on file structure and where program is called from
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from read_write import *
from my_function import *

READ_MODE = 1
WRITE_MODE = 2


# Define file names as strings here
ifile = "supporting_files/sin_wave.pak52"
ofile = "test.bin"

def assert_binpak_data_equal(a, b):
    # Basic fields
    assert a.nx == b.nx, f"nx mismatch: {a.nx} != {b.nx}"
    assert a.nz == b.nz, f"nz mismatch: {a.nz} != {b.nz}"
    assert a.xCplx == b.xCplx, f"xCplx mismatch: {a.xCplx} != {b.xCplx}"
    assert a.yCplx == b.yCplx, f"yCplx mismatch: {a.yCplx} != {b.yCplx}"
    assert a.zCplx == b.zCplx, f"zCplx mismatch: {a.zCplx} != {b.zCplx}"
    assert a.name == b.name, f"name mismatch: {a.name} != {b.name}"
    # xdata
    for i in range(a.nx):
        assert a.xdata[i] == b.xdata[i], f"xdata[{i}] mismatch: {a.xdata[i]} != {b.xdata[i]}"
    # zdata
    for i in range(a.nz):
        assert a.zdata[i] == b.zdata[i], f"zdata[{i}] mismatch: {a.zdata[i]} != {b.zdata[i]}"
    # ydata (2D)
    for z in range(a.nz):
        for x in range(a.nx):
            assert a.ydata[z][x] == b.ydata[z][x], f"ydata[{z}][{x}] mismatch: {a.ydata[z][x]} != {b.ydata[z][x]}"

class TestBinPakData(unittest.TestCase):
    def test_fully_cycle(self):
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
        # Convert to Python and apply filter
        y_array = ydata_to_np_array(data)
        x_array = xdata_to_np_array(data)
        z_array = zdata_to_np_array(data)

        filtered_ydata = apply_gaussian_filter(y_array)
        filtered_xdata = apply_gaussian_filter(x_array)
        filtered_zdata = apply_gaussian_filter(z_array)

        # Convert back to binPakData format by creating new BinPakData structure and copying values
        new_filtered_data_ptr = copy_bin_data(data, filtered_xdata, filtered_ydata, filtered_zdata)

        py_write_one_data_set(df_o, new_filtered_data_ptr)

        # full cycle
        df_read2 = py_open_pak_bin_file(ofile, ctypes.byref(n_data_arrays), READ_MODE)
        py_read_data_set_header(df_read2, ctypes.byref(n_data_sets))
        read2_data_set_ptr = py_read_one_data_set(df_read2)

        assert_binpak_data_equal(new_filtered_data_ptr.contents, read2_data_set_ptr.contents)

        py_free_bin_pak_data(in_data_set_ptr)
        py_close_pak_bin_file(df_i)
        py_close_pak_bin_file(df_o)
        py_free_bin_pak_data(read2_data_set_ptr)
        py_close_pak_bin_file(df_read2)

if __name__ == "__main__":
    unittest.main()
