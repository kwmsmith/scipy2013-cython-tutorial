#-----------------------------------------------------------------------------
# Copyright (c) 2012, Enthought, Inc.
# All rights reserved.  See LICENSE.txt for details.
# 
# Author: Kurt W. Smith
# Date: 26 March 2012
#-----------------------------------------------------------------------------

from time import time
import numpy as np

def compute_julia(c, N, bound=2, lim=1000.):
    ''' Pure Python calculation of the Julia set for a given `c` using NumPy
    array operations.
    '''
    orig_err = np.seterr()
    np.seterr(over='ignore', invalid='ignore')
    julia = np.zeros((N, N), dtype=np.uint32)
    X, Y = np.ogrid[-bound:bound:N*1j, -bound:bound:N*1j]
    iterations = X + Y * 1j
    count = 0
    esc_mask = np.zeros_like(julia, dtype=bool)
    t0 = time()
    while not np.all(esc_mask):
        new_esc_mask = ~esc_mask & (np.abs(iterations) >= lim)
        julia[new_esc_mask] = count
        esc_mask |= new_esc_mask
        count += 1
        iterations = iterations**2 + c
    np.seterr(**orig_err)
    return julia, time() - t0

