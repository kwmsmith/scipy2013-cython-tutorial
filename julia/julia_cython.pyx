#-----------------------------------------------------------------------------
# Copyright (c) 2012, 2013, Enthought, Inc.
# All rights reserved.  Distributed under the terms of the 2-clause BSD
# licence.  See LICENSE.txt for details.
# 
# Author: Kurt W. Smith
# Date: 26 March 2012
#-----------------------------------------------------------------------------

# --- Python std lib imports -------------------------------------------------
from time import time
import numpy as np

# --- Cython cimports --------------------------------------------------------
cimport cython
from cython.parallel cimport prange
from libc.stdint cimport uint32_t, int32_t

# --- Ctypedefs --------------------------------------------------------

ctypedef float     real_t
ctypedef uint32_t  uint_t
ctypedef int32_t   int_t

#-----------------------------------------------------------------------------
# Cython functions
#-----------------------------------------------------------------------------
def abs_sq(zr, zi):
    return zr * zr + zi * zi

def kernel(zr, zi, cr, ci, lim, cutoff):
    ''' 
    Cython implementation of the kernel computation; major opportunites for
    speedups here...

    '''
    count = 0
    lim_sq = lim * lim
    while abs_sq(zr, zi) < lim_sq and count < cutoff:
        zr, zi = zr * zr - zi * zi + cr, 2 * zr * zi + ci
        count += 1
    return count

def compute_julia(cr, ci, N, bound=1.5, lim=1000., cutoff=1e6):
    ''' 
    Calls `kernel()` for each location in the numpy array `julia`.

    Your job is to speed this up!

    '''
    
    julia = np.empty((N, N), dtype=np.uint32)
    grid = np.asarray(np.linspace(-bound, bound, N), dtype=np.float32)
    t0 = time()
    for i in range(N):
        x = grid[i]
        for j in range(N):
            y = grid[j]
            julia[i,j] = kernel(x, y, cr, ci, lim, cutoff)
    return julia, time() - t0
