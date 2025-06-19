# Author: Zach Philip
# Date: June 2nd, 2025
# Property of Whisper Aero

#################################################################################
# Ctype to wrap binPakData structure from provided Mueller rw_data.h file       #
# Note: be sure to free memory when needed                                      # 
#################################################################################

import ctypes

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
