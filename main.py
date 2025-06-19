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
from my_function import *

# needed so debugger can find read_write.py for imports 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from read_write import *

READ_MODE = 1
WRITE_MODE = 2

# ============= DO NOT EDIT ABOVE THIS LINE ============== #
# Use file names as strings if not running from the command line
# Define file names as strings here: syntax is "filename.ext"
# ifile = "sin_wave.pak52"
# ifile = "output.bin"
# ofile = "filtered_data.bin"

# ============= DO NOT EDIT BELOW THIS LINE ============== #

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

    y_array = ydata_to_np_array(data)

    # ========== DO NOT EDIT ABOVE THIS LINE =========== #

    # Apply filter using my_function file
    filtered_data = apply_gaussian_filter(y_array)

    # ========== DO NOT EDIT BELOW THIS LINE =========== #

    data = np_array_to_ydata(filtered_data, data)
    py_write_one_data_set(df_o, in_data_set_ptr)

    # be sure to free memory after use
    py_free_bin_pak_data(in_data_set_ptr) 
    py_close_pak_bin_file(df_i)
    py_close_pak_bin_file(df_o)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)