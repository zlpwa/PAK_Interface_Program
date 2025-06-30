# Author: Zach Philip
# Date: June 2nd, 2025
# Property of Whisper Aero

#################################################################################
# This file uses the DLL from the rw_data.c code to read and write data         #
# from a binary file in the PAK format. It provides Python wrappers for the c   #
# functions. Note: not all functions are required to be called as they call     #
# each other internally. This file also includes functions to convert data to   #
# and from numpy arrays                                                         #
#################################################################################

import ctypes
import os
import sys
import numpy as np

# Mirrors structure from rw_data.c
class BinPakData(ctypes.Structure):
    _fields_ = [
        ('name', ctypes.c_char * 256),                              # char name[256]
        ('xCplx', ctypes.c_int),                                    # int xCplx
        ('nx', ctypes.c_long),                                      # long nx
        ('xdata', ctypes.POINTER(ctypes.c_double)),                 # double *xdata
        ('zCplx', ctypes.c_int),                                    # int zCplx
        ('nz', ctypes.c_long),                                      # long nz
        ('zdata', ctypes.POINTER(ctypes.c_double)),                 # double *zdata
        ('yCplx', ctypes.c_int),                                    # int yCplx
        ('ydata', ctypes.POINTER(ctypes.POINTER(ctypes.c_double)))  # double **ydata
    ]


# Load DLL
# Base path is root directory and is joined with dll_path
# If you change file structure, you may need to change this
base_path = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(base_path, "pak_lib.dll")
if sys.platform == "win32":
    os.add_dll_directory(os.path.dirname(dll_path))
pak_lib = ctypes.CDLL(dll_path)


# Explicitly declare parameter and return types of functions in DLL
# ========================== File/Memory Handling ===========================
# void closePakBinFile(int df);
pak_lib.closePakBinFile.argtypes = [ctypes.c_int]
pak_lib.closePakBinFile.restype = None

# void freeBinPakData(struct binPakData* pData);
pak_lib.freeBinPakData.argtypes = [ctypes.POINTER(BinPakData)]
pak_lib.freeBinPakData.restype = None

# int openPakBinFile(char *filename, short *nDataArrays, int oMode);
pak_lib.openPakBinFile.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_short), ctypes.c_int]
pak_lib.openPakBinFile.restype = ctypes.c_int

# ========================== Reads ===========================
# struct binPakData *readDataSetData(int df);
pak_lib.readDataSetData.argtypes = [ctypes.c_int]
pak_lib.readDataSetData.restype = ctypes.POINTER(BinPakData)

# int readDataSetHeader(int df, long *nDataSets);
pak_lib.readDataSetHeader.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_long)]
pak_lib.readDataSetHeader.restype = ctypes.c_int

# int readDataSetName(int df, char *dsName);
pak_lib.readDataSetName.argtypes = [ctypes.c_int, ctypes.c_char_p]
pak_lib.readDataSetName.restype = ctypes.c_int

# int readDataSetDataInfo(int df, int *cplx, long *nVal);
pak_lib.readDataSetDataInfo.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_long)]
pak_lib.readDataSetDataInfo.restype = ctypes.c_int

# double *readDataSetDataValues(int df, int cplx, long nVal);
pak_lib.readDataSetDataValues.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_long]
pak_lib.readDataSetDataValues.restype = ctypes.POINTER(ctypes.c_double)

# struct binPakData *readOneDataSet(int df);
pak_lib.readOneDataSet.argtypes = [ctypes.c_int]
pak_lib.readOneDataSet.restype = ctypes.POINTER(BinPakData)

# ========================== Writes ===========================
# int writeDataSetData(int df, struct binPakData *pData);
pak_lib.writeDataSetData.argtypes = [ctypes.c_int, ctypes.POINTER(BinPakData)]
pak_lib.writeDataSetData.restype = ctypes.c_int

# int writeDataSetHeader(int df, long nDataSets);
pak_lib.writeDataSetHeader.argtypes = [ctypes.c_int, ctypes.c_long]
pak_lib.writeDataSetHeader.restype = ctypes.c_int

# int writeDataSetName(int df, char *dsName);
pak_lib.writeDataSetName.argtypes = [ctypes.c_int, ctypes.c_char_p]
pak_lib.writeDataSetName.restype = ctypes.c_int

# int writeDataSetDataInfo(int df, int cplx, long nVal);
pak_lib.writeDataSetDataInfo.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_long]
pak_lib.writeDataSetDataInfo.restype = ctypes.c_int

# int writeDataSetDataValues(int df, int cplx, long nVal, double *data);
pak_lib.writeDataSetDataValues.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_long, ctypes.POINTER(ctypes.c_double)]
pak_lib.writeDataSetDataValues.restype = ctypes.c_int

# int writeOneDataSet(int df, struct binPakData *pData);
pak_lib.writeOneDataSet.argtypes = [ctypes.c_int, ctypes.POINTER(BinPakData)]
pak_lib.writeOneDataSet.restype = ctypes.c_int

# int writePakBinFileHeader(int df, short nDataArrays);
pak_lib.writePakBinFileHeader.argtypes = [ctypes.c_int, ctypes.c_short]
pak_lib.writePakBinFileHeader.restype = ctypes.c_int

# Python wrappers that call DLL functions
# ============= File/Memory handling ===============
def py_open_pak_bin_file(filename, n_data_arrays, o_mode):
    if isinstance(filename, str):
        filename = filename.encode('utf-8')
    df = pak_lib.openPakBinFile(filename, n_data_arrays, o_mode)
    if df < 0:
        raise FileNotFoundError(f"Failed to open input file: {filename}")
    return df
    
def py_close_pak_bin_file(df):
    return pak_lib.closePakBinFile(df)

def py_free_bin_pak_data(pdata):
    return pak_lib.freeBinPakData(pdata)

# ==================== READS ====================
def py_read_data_set_data(df):
    return pak_lib.readDataSetData(df) 

def py_read_data_set_header(df, n_data_sets):
    ret = pak_lib.readDataSetHeader(df, n_data_sets)
    if ret < 0:
        raise RuntimeError("Failed to read data set header")
    return ret

def py_read_data_set_name(df, ds_name):
    return pak_lib.readDataSetName(df, ds_name)

def py_read_data_set_data_info(df, cplx, n_val):
    return pak_lib.readDataSetDataInfo(df, cplx, n_val)

def py_read_data_set_data_values(df, cplx, n_val):
    return pak_lib.readDataSetDataValues(df, cplx, n_val)

# be sure to free memory after using the function below: py_read_one_data_set
def py_read_one_data_set(df):
    p_data = pak_lib.readOneDataSet(df)
    if not p_data:
        raise RuntimeError("Failed to read one data set")
    if p_data.contents.nz != 1:
        raise ValueError("This program only works with nz = 1, got nz = {}".format(p_data.contents.nz)) 

    return p_data

# ==================== WRITES ====================
def py_write_data_set_data(df, pdata):
    return pak_lib.writeDataSetData(df, pdata)

def py_write_data_set_header(df, n_data_sets):
    ret = pak_lib.writeDataSetHeader(df, n_data_sets)
    if ret < 0:
        raise RuntimeError("Failed to write data set header")
    return ret

def py_write_data_set_name(df, ds_name):
    if isinstance(ds_name, str):
        ds_name = ds_name.encode('utf-8')
    return pak_lib.writeDataSetName(df, ds_name)

def py_write_data_set_data_info(df, cplx, n_val):
    return pak_lib.writeDataSetDataInfo(df, cplx, n_val)

def py_write_data_set_data_values(df, cplx, n_val, data):
    return pak_lib.writeDataSetDataValues(df, cplx, n_val, data)

def py_write_one_data_set(df, pdata):
    ret = pak_lib.writeOneDataSet(df, pdata)
    if ret < 0:
        raise RuntimeError("Failed to write one data set")
    return ret

def py_write_pak_bin_file_header(df, n_data_arrays):
    ret = pak_lib.writePakBinFileHeader(df, n_data_arrays)
    if ret < 0:
        raise RuntimeError("Failed to write PAK bin file header")
    return ret

# Functions to convert binPakData to numpy arrays and vice versa
# Y DATA
def ydata_to_np_array(data):
    nx = data.nx
    ydata = data.ydata.contents
    y_array1 = np.zeros(nx, dtype = np.float64)
    for i in range(nx):
        y_array1[i] = ydata[i]
    return y_array1

def np_array_to_ydata(filtered_data):
    filt_ydata_array = (ctypes.c_double * filtered_data.size)()
    for i in range(filtered_data.size):
        filt_ydata_array[i] = filtered_data[i]
    return filt_ydata_array

# X DATA
def xdata_to_np_array(data):
    nx = data.nx
    xdata = data.xdata
    x_array1 = np.zeros(nx, dtype = np.float64)
    for i in range(nx):
        x_array1[i] = xdata[i]
    return x_array1

def np_array_to_xdata(filtered_data):
    filt_xdata_array = (ctypes.c_double * filtered_data.size)()
    for i in range(filtered_data.size):
        filt_xdata_array[i] = filtered_data[i]
    return filt_xdata_array

# Z DATA
def zdata_to_np_array(data):
    nz = data.nz
    zdata = data.zdata
    z_array1 = np.zeros(nz, dtype = np.float64)
    for i in range(nz):
        z_array1[i] = zdata[i]
    return z_array1

def np_array_to_zdata(filtered_data):
    filt_zdata_array = (ctypes.c_double * filtered_data.size)()
    for i in range(filtered_data.size):
        filt_zdata_array[i] = filtered_data[i]
    return filt_zdata_array


def copy_bin_data(data, filtered_x_data, filtered_y_data, filtered_z_data):
    # Create object in Python so do not have to free it 
    new_data_ptr = ctypes.pointer(BinPakData())
    new_data = new_data_ptr.contents

    new_data.name = data.name
    new_data.nz = filtered_z_data.size
    new_data.nx = filtered_x_data.size
    new_data.xCplx = data.xCplx
    new_data.zCplx = data.zCplx
    new_data.yCplx = data.yCplx

    # X DATA
    x_ptr = np_array_to_xdata(filtered_x_data)
    new_data.xdata = ((ctypes.c_double) * 1)()
    new_data.xdata = x_ptr 

    # Y DATA
    y_ptr_0 = np_array_to_ydata(filtered_y_data)
    new_data.ydata = (ctypes.POINTER(ctypes.c_double) * 1)()
    new_data.ydata[0] = y_ptr_0 

    # Z DATA
    z_ptr = np_array_to_zdata(filtered_z_data)
    new_data.zdata = ((ctypes.c_double) * 1)()
    new_data.zdata = z_ptr

    return new_data_ptr

# Function to print the contents of BinPakData for testing
def print_bin_pak_data(data): 
    print(f"Name     : {data.name.decode('utf-8') if data.name else None}")
    print(f"nx       : {data.nx}")
    print(f"nz       : {data.nz}")
    print(f"xCplx    : {data.xCplx}")
    print(f"yCplx    : {data.yCplx}")
    print(f"zCplx    : {data.zCplx}")
    print()
    print("xdata:")
    for i in range(data.nx):
        print(f"  x[{i}] = {data.xdata[i]}")
    print()
    print("ydata:")
    for z in range(data.nz):
        print(f"  y[{z}]:")
        for i in range(data.nx):
            print(f"    y[{z}][{i}] = {data.ydata[z][i]}")
    print()
    print("zdata:")
    for i in range(data.nz):
        print(f"  z[{i}] = {data.zdata[i]}")


