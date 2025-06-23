# Author: Zach Philip
# Date: June 2nd, 2025
# Property of Whisper Aero

#################################################################################
# This file is called from main and is used to scale the ydata using python     #
# packages. Import packages and define the functions below. This program relies #
# on nz = 1 and only allows for the scaling of ydata.                           #
#################################################################################

# May need to add imports
from scipy.ndimage import gaussian_filter1d # EXAMPLE

# EXAMPLE
def apply_gaussian_filter(y_array, sigma = 2): 
    return gaussian_filter1d(y_array, sigma = sigma)

#######################################################
# Add any additional functions you need below this line