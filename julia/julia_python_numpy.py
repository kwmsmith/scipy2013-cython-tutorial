#-----------------------------------------------------------------------------
# Copyright (c) 2012, Enthought, Inc.
# All rights reserved.  See LICENSE.txt for details.
# 
# Author: Kurt W. Smith
# Date: 26 March 2012
#-----------------------------------------------------------------------------

'''
The Julia set calculation using only numpy array expressions and masks: no for
loops or if statements necessary!  Your task is to complete 
'''

from time import time
import numpy as np

def compute_julia(c, N, bound=2, lim=1000.):
    ''' Pure Python calculation of the Julia set for a given `c` using NumPy
    array operations.
    '''

    # The following lines are to turn off warnings during computation; we
    # restore the warnings afterwards.
    orig_err = np.seterr()
    np.seterr(over='ignore', invalid='ignore')

    # Initialize the result array and the domain over which the Julia set is to
    # be computed.
    julia = np.zeros((N, N), dtype=np.uint32)
    X, Y = np.ogrid[-bound:bound:N*1j, -bound:bound:N*1j]

    # iterations will be iterated inside the while loop according to the julia set computation:
    #     iterations = iterations**2 + c
    iterations = X + Y * 1j

    # Stores the number of times through the while loop thus far.
    count = 0

    # A boolean mask array that is true for all locations that have escaped
    # (iterated past the limit).
    esc_mask = np.zeros_like(julia, dtype=bool)

    # start the timer
    t0 = time()
    while not np.all(esc_mask):

        # new_esc_mask holds all the *newly* escaped locations during *this iteration*.

        # TODO: fill in the right-hand-side of new_esc_mask.  
        # Hint: it is composed of the logical conjunction of the locations that
        # haven't escaped so far and the locations in `iterations` that have
        # exceeded `lim`.
        new_esc_mask = ...

        # Update the `julia` result array at the newly escaped locations.
        # TODO: fill in the array mask (a single variable) and the RHS (a
        # single variable).
        julia[...] = ...

        # incorporate the newly escaped locations into `esc_mask`.
        # TODO: fill in the RHS (a single variable).
        esc_mask |= ...

        # update the count
        count += 1

        # The core julia set calcualtion using NumPy array expressions.
        # TODO: fill in the RHS to perform the core Julia set computation.
        iterations = ...

    np.seterr(**orig_err)
    return julia, time() - t0
