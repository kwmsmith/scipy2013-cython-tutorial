#-----------------------------------------------------------------------------
# Copyright (c) 2012, Enthought, Inc.
# All rights reserved.  See LICENSE.txt for details.
# 
# Author: Kurt W. Smith
# Date: 26 March 2012
#-----------------------------------------------------------------------------

# --- Python / Numpy imports -------------------------------------------------
import multiprocessing as mp
from time import time
import numpy as np

# --- Local imports ----------------------------------------------------------
from julia_pure_python import kernel

def compute_julia_section(args):
    '''
    Computes a section of the julia set.  
    
    This is the workhorse function designed to work with
    multiprocessing.Pool.map(), which explains why it takes a single argument
    tuple that must be unpacked, rather than an argument list.
    
    Arguments
    ---------

    `args` is an argument tuple; the expected order is:

        grid_x, grid_y, c, lim, kernel = args

    grid_x, grid_y: the x & y domains on which to compute the julia set.
    c, lim: arguments to pass to the kernel function.
    kernel: the julia kernel computation.

    Returns
    -------

    The section of the julia set on the domain [grid_x X grid_y].

    '''
    # unpack the argument tuple.
    grid_x, grid_y, c, lim, kernel = args
    # extract nx & ny.
    nx, ny = grid_x.shape[0], grid_y.shape[0]
    # make grid_y purely imaginary.
    grid_y = grid_y * 1j
    # initialize the result array.
    julia = np.empty((nx, ny), dtype=np.uint32)
    c = complex(c)
    for i, x in enumerate(grid_x):
        for j, y in enumerate(grid_y):
            julia[i,j] = kernel(x+y, c, lim)
    return julia


def compute_julia(c, N, bound=2, lim=1000., kernel=kernel, num_sections=8):
    '''
    Computes the julia set for an NxN complex domain using Python's
    multiprocessing module for parallelization.

    Note: this version breaks up the domain over the first dimension;
    improvements to the computation would be to break up the computation over
    both the first and second dimensions.

    Arguments
    ---------

    c: The complex parameter for the Julia set computation.

    N: number of grid points in each dimension

    bound: the boundary of the domain in each dimension.

    lim: cutoff limit for the Julia set computation.

    kernel: the kernel function to use.

    num_sections: approximate number of sections to split domain into, this
    will be modified upwards until it is a factor of N.

    Returns
    -------

    The Julia set computed on the complex domain (-bound, bound) X (-bound,
    bound) of shape (N, N).

    '''
    # adjust num_sections upwards until it's a factor of N.  Doing so ensures
    # that N is divided into equal sections, and significantly simplifies the
    # rest of the code.
    while N % num_sections:
        num_sections += 1

    # The grid locations on which to run the computation.  The grid will be
    # split over the x dimension (rows).
    grid = np.linspace(-bound, bound, N)
    chunk = N / num_sections

    # The sections of the grid split over rows, in `chunk` sizes.
    grid_x_sections = [grid[i*chunk:(i+1)*chunk] for i in range(num_sections)]

    # create a list of argument tuples to pass to compute_julia_section().
    # Each argument tuple is identical except for the grid_x_section argument.
    # Wrapping everything in an argument tuple is required by the map()
    # function interface.
    compute_julia_section_args = [(grid_x, grid, c, lim, kernel) 
                                    for grid_x in grid_x_sections]

    # Here is where we use a task pool from multiprocessing.
    pool = mp.Pool()

    # Start the timer.
    t0 = time()

    # This will block until all computations are run. Pool.map() automatically
    # handles load balancing for us in a simple way.
    julia_sections = pool.map(compute_julia_section, compute_julia_section_args)

    # The result of compute_julia_section() is a section of the final array; we
    # have to concatenate() them along the 0th axis to create the final julia
    # array.
    julia = np.concatenate(julia_sections, axis=0)

    # Stop the timer.
    t1 = time() - t0

    # Ensure that the shape is correct.
    assert julia.shape == (N, N)
    return julia, t1

def compute_julia_block(c, N, bound=2, lim=1000., kernel=kernel, num_sections=8):
    '''
    Computes the julia set for an NxN complex domain using Python's
    multiprocessing module for parallelization.

    This is an alternative implementation of compute_julia().
    compute_julia_block() breaks up the domain over both the x and y dimensions
    rather than just the x dimension.

    Arguments
    ---------

    c: The complex parameter for the Julia set computation.

    N: number of grid points in each dimension

    bound: the boundary of the domain in each dimension.

    lim: cutoff limit for the Julia set computation.

    kernel: the kernel function to use.

    num_sections: approximate number of sections to split domain into, this
    will be modified upwards until it is a factor of N.

    Returns
    -------

    The Julia set computed on the complex domain (-bound, bound) X (-bound,
    bound) of shape (N, N).

    '''
    # adjust num_sections upwards until it's a factor of N.  Doing so ensures
    # that N is divided into equal sections, and significantly simplifies the
    # rest of the code.
    while N % num_sections:
        num_sections += 1

    # The grid locations on which to run the computation.  The grid will be
    # split over the x dimension (rows).
    grid = np.linspace(-bound, bound, N)
    chunk = N / num_sections

    # The sections of the grid split over rows, in `chunk` sizes.
    grid_x_sections = [grid[i*chunk:(i+1)*chunk] for i in range(num_sections)]

    # The sections of the grid split over rows, in `chunk` sizes.
    grid_y_sections = grid_x_sections

    # create a list of argument tuples to pass to compute_julia_section().
    # Wrapping everything in an argument tuple is required by the map()
    # function interface.
    compute_julia_section_args = [(grid_x, grid_y, c, lim, kernel) 
                                    for grid_x in grid_x_sections
                                    for grid_y in grid_y_sections]

    # Here is where we use a task pool from multiprocessing.
    pool = mp.Pool()

    # Start the timer.
    t0 = time()

    # This will block until all computations are run. Pool.map() automatically
    # handles load balancing for us in a simple way.
    julia_sections = pool.map(compute_julia_section, compute_julia_section_args)

    # The result of compute_julia_section() is a section of the final array; we
    # have to concatenate() them along the 0th axis to create the final julia
    # array.
    julia = np.empty((N, N), dtype=np.uint32)
    for i in range(num_sections):
        for j in range(num_sections):
            julia[i*chunk:(i+1)*chunk, j*chunk:(j+1)*chunk] = julia_sections[i*num_sections+j]

    # Stop the timer.
    t1 = time() - t0

    # Ensure that the shape is correct.
    assert julia.shape == (N, N)
    return julia, t1
