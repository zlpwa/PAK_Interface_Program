# Author: Zach Philip
# Date: June 2nd, 2025
# Property of Whisper Aero

#################################################################################
# This file is called from main and is used to scale the ydata using python     #
# packages. Import packages and define the functions below. This program relies #
# on nz = 1.                                                                    #
#################################################################################

# May need to add imports
from scipy.ndimage import gaussian_filter1d # EXAMPLE
import numpy as np

# EXAMPLE
def apply_gaussian_filter(arr, sigma = 2): 
    return gaussian_filter1d(arr, sigma = sigma)

def ex_diff(arr):
    return np.diff(arr)

def ex_a_range(arr):
    return np.arange(len(arr)/5)

def filter_below_threshold(arr, threshold=0.5):
    return arr[arr <= threshold]

#######################################################
# Add any additional functions you need below this line

