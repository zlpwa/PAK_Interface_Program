# Author: Zach Philip
# Date: June 2nd, 2025
# Property of Whisper Aero

#################################################################################
# This file is the driver to open binary files, read the data, scale it in      #
# python, and write it to an output file. This program relies on nz = 1,        #
# n_data_arrays = 1, n_data_sets = 1. The program is easily adaptable, however, #
# if one of those assumptions does not hold.                                    #
#################################################################################

import sys
import os
import ctypes


# Line below needed in some instances depending on file structure and where program is called from
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.read_write import *
from src.my_function import *

READ_MODE = 1
WRITE_MODE = 2

# If number of arguements change, process those here.
if len(sys.argv) != 3:
    print("[ERROR] Usage: python main.py <input_file.bin> <output_file.bin>")
    sys.exit(1)
ifile = sys.argv[1]
ofile = sys.argv[2]

def main():
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

    # Convert to Python (do this for each data array even if not scaling)
    y_array = ydata_to_np_array(data)
    x_array = xdata_to_np_array(data)
    z_array = zdata_to_np_array(data)

    # ============= EDIT BELOW THIS LINE =============
    # Change filter here (if not applying a filter, just assign the array directly i.e. filtered_ydata = y_array)
    filtered_ydata = apply_gaussian_filter(y_array)
    filtered_xdata = apply_gaussian_filter(x_array)
    filtered_zdata = apply_gaussian_filter(z_array)

    # ============= EDIT ABOVE THIS LINE =============

    # Create new BinPakData object for filtered data
    new_filtered_data_ptr = copy_bin_data(data, filtered_xdata, filtered_ydata, filtered_zdata)

    py_write_one_data_set(df_o, new_filtered_data_ptr)

    # Free memory after use (no need to free new_filtered_data_ptr as it is not allocated in C)
    py_free_bin_pak_data(in_data_set_ptr) 
    py_close_pak_bin_file(df_i)
    py_close_pak_bin_file(df_o)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)