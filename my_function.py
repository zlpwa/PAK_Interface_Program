# Author: Zach Philip
# Date: June 2nd, 2025
# Property of Whisper Aero

#################################################################################
# This file is called from main and is used to scale the ydata using python     #
# packages. Import packages and define the functions below. This program relies #
# on nz = 1 and only allows for the scaling of ydata.                           #
#################################################################################

# May need to add imports
import numpy as np
from scipy.ndimage import gaussian_filter1d # EXAMPLE
from scipy.signal import butter, filtfilt


# DO NOT MODIFY THE FUNCTION BELOW
def ydata_to_np_array(data):
    nx = data.nx
    ydata = data.ydata.contents
    y_array1 = np.zeros(nx, dtype = np.float64)
    for i in range(nx):
        y_array1[i] = ydata[i]
    return y_array1

# DO NOT MODIFY THE FUNCTION BELOW
def np_array_to_ydata(filtered_data, data):
    ydata = data.ydata.contents
    for i in range(filtered_data.size):
        ydata[i] = filtered_data[i]
    data.ydata.contents = ydata
    return data

# EXAMPLE
def apply_gaussian_filter(y_array, sigma = 2): 
    return gaussian_filter1d(y_array, sigma = sigma)

#######################################################
# Add any additional functions you need below this line