#-----------------------------------------------------------------------------
# Copyright (c) 2012, Enthought, Inc.
# All rights reserved.  See LICENSE.txt for details.
# 
# Author: Kurt W. Smith
# Date: 26 March 2012
#-----------------------------------------------------------------------------

# --- Python / Numpy imports -------------------------------------------------
import numpy as np
from time import time

def kernel(z, lim, cutoff=1e6):
    ''' Computes the number, `n`, of iterations necessary such that 
    |z_n| > `lim`, where `z_n = z_{n-1}**2 + c`.
    '''
    count = 0
    u = z
    while abs(u) < lim and count < cutoff:
        u = u * u + z
        count += 1
    return count

def compute_mandelbrot(N, bound=1.5, lim=1000., cutoff=1e6, kernel=kernel):
    ''' Pure Python calculation of the Julia set for a given `c`.  No NumPy
        array operations are used.
    '''
    
    mandel = np.empty((N, N), dtype=np.uint32)
    grid_x = np.linspace(-bound, bound, N)
    grid_y = grid_x * 1j
    t0 = time()
    for i, x in enumerate(grid_x):
        for j, y in enumerate(grid_y):
            mandel[i,j] = kernel(x+y, lim, cutoff=cutoff)
    return mandel, time() - t0
