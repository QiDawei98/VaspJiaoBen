# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 22:36:52 2025

@author: qidaw
"""

"""
Converts Cartesian coordinates to fractional coordinates.

Then, tests whether a given point is in the unit cell.
"""

import numpy as np
a = np.array([5.676662, 0, 0])
b = np.array([0, 5.676662, 0])
c = np.array([0, 0, 5.676662])
M = np.column_stack((a, b, c))

def cart2frac(x, y, z):
    M_inv = np.linalg.inv(M)
    return np.dot(M_inv, np.array([x, y, z]))
    
def incell(x, y, z):
    frac_coor = cart2frac(x, y, z)
    return np.all((frac_coor >= 0) & (frac_coor <= 1))

print(incell(1, 2, 3))