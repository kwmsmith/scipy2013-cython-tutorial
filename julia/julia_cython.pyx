#-----------------------------------------------------------------------------
# Copyright (c) 2012, Enthought, Inc.
# All rights reserved.  See LICENSE.txt for details.
# 
# Author: Kurt W. Smith
# Date: 26 March 2012
#-----------------------------------------------------------------------------

'''
Your task in this file is primarily to add type information to the functions
below to help speed up the generated extension module.  First read through the
source code to gain an understanding of what is going on; compare with the
julia_pure_python.py file if need be.  The comments marked with "TODO" indicate
what you need to do for the exercise.
'''

# --- Python std lib imports -------------------------------------------------
from time import time
import numpy as np

# --- Cython cimports --------------------------------------------------------
cimport cython
from libc.stdlib cimport free
from cpython.cobject cimport PyCObject_FromVoidPtr
cimport numpy as cnp

# --- Local Ctypedefs --------------------------------------------------------
# Necessary to declare these typedefs here (not in the cdef extern block).
# NOTE: Make sure these stay in sync with the _julia_ext.h header typedefs!!

ctypedef double complex cpx_t
ctypedef double         real_t

# Necessary to call `np.import_array()` before calling functions from the NumPy
# C-API.
cnp.import_array()

#-----------------------------------------------------------------------------
# Cython functions
#-----------------------------------------------------------------------------
cpdef unsigned int kernel(z, c, lim, cutoff=1e6):
    ''' Cython implementation of the kernel computation.

    This is implemented so that no C-API calls are made inside the function
    body.  Even still, there is some overhead as compared with a pure C
    implementation.
    '''
    #-------------------------------------------------------------------------
    # TODO: Add type information to the function arguments and to the local
    # variables lim_sq and count.
    #-------------------------------------------------------------------------
    count = 0
    lim_sq = lim * lim
    while cabs_sq(z) < lim_sq and count < cutoff:
        z = z * z + c
        count += 1
    return count

def compute_julia_no_opt(c, N, bound=1.5, lim=1000.):
    ''' 
    Cythonized version of a pure Python implementation of the compute_julia()
    function.  It uses numpy arrays, but does not use any extra syntax to speed
    things up beyond simple type declarations.

    '''
    #-------------------------------------------------------------------------
    # TODO: Add type information to the function arguments and to the local
    # variables i, j, x, and y.
    #-------------------------------------------------------------------------
    julia = np.empty((N, N), dtype=np.uint32)
    grid = np.linspace(-bound, bound, N)
    t0 = time()
    for i in range(N):
        x = grid[i]
        for j in range(N):
            y = grid[j]
            julia[i,j] = kernel(x+y*1j, c, lim)
    return julia, time() - t0

cdef inline real_t cabs_sq(cpx_t z):
    ''' Helper inline function, computes the square of the abs. value of the
    complex number `z`.
    '''
    return z.real * z.real + z.imag * z.imag


def compute_julia_opt(c, N, bound=1.5, lim=1000.):
    '''
    Cython `compute_julia()` implementation with Numpy array buffer
    declarations and appropriate compiler directives.  The body of this
    function is nearly identical to the `compute_julia_no_opt()` function.

    '''
    #-------------------------------------------------------------------------
    # TODO: Add type information to the function arguments and to the local
    # variables i, j, x, y.
    #
    # Add type information for the numpy arrays `julia` and `grid`.  The
    # `julia` array is already done for you.
    #
    # Add function decorators to turn off boundschecking and wraparound
    # checking.  The decorators are listed below.
    # cython.boundscheck(False)
    # cython.wraparound(False)
    #-------------------------------------------------------------------------

    cdef cnp.ndarray[cnp.uint32_t, ndim=2, mode='c'] julia 

    julia = np.empty((N, N), dtype=np.uint32)
    grid = np.linspace(-bound, bound, N)
    t0 = time()
    for i in range(N):
        x = grid[i]
        for j in range(N):
            y = grid[j]
            julia[i,j] = kernel(x+y*1j, c, lim)
    return julia, time() - t0

#-----------------------------------------------------------------------------
# Everything below relates to Cython wrapping external code.  It is included
# here for reference to show you how to properly wrap and call external
# functions and deal with memory cleanup when you're done with an externally
# allocated array.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# External declarations
#-----------------------------------------------------------------------------
cdef extern from "_julia_ext.h" nogil:

    unsigned int ext_julia_kernel "julia_kernel"(cpx_t, cpx_t, 
                                                 real_t, real_t)
    unsigned int *ext_compute_julia "compute_julia"(cpx_t, unsigned int,
                                               real_t, real_t)


def compute_julia_ext(cpx_t c,
                       unsigned int N,
                       real_t bound=1.5,
                       real_t lim=1000.):
    '''
    Call an externally implemented version of `compute_julia()` and wrap the
    resulting C array in a NumPy array.

    '''
    t0 = time()
    cdef unsigned int *julia = ext_compute_julia(c, N, bound, lim)
    cdef cnp.npy_intp dims[2]
    dims[0] = N; dims[1] = N
    arr = new_array_owns_data_cython(2, dims, cnp.NPY_UINT, <void*>julia)
    return arr, time() - t0


cdef void local_free(void *data):
    ''' Wraps `free()` from C's stdlib with some output to indicate that it's
    been called.
    '''
    free(data)

cdef object new_array_owns_data(int nd,
                                cnp.npy_intp *dims,
                                int typenum,
                                void *data):
    ''' Creates a Numpy array with data from the `data` buffer.  Sets the array
    base appropriately using `PyCObject_FromVoidPtr()` to ensure that the data
    gets cleaned up when the Numpy array object is garbage collected.

    '''
    arr = cnp.PyArray_SimpleNewFromData(nd, dims, typenum, data)
    cnp.set_array_base(arr, PyCObject_FromVoidPtr(data, local_free))
    return arr

cdef class _dealloc_shim:
    ''' Deallocation shim class that exists simply to free() the _data pointer.
    '''
    cdef void *_data

    def __cinit__(self):
        self._data = NULL

    def __dealloc__(self):
        if self._data:
            free(self._data)
        self._data = NULL

cdef object new_array_owns_data_cython(int nd,
                                       cnp.npy_intp *dims,
                                       int typenum,
                                       void *data):
    ''' Same as `new_array_owns_data()`, but uses a `_dealloc_shim` instance
    rather than `PyCObject_FromVoidPtr()`.  This solution is usable from all
    Python versions (Python 2 and 3), whereas PyCObject_FromVoidPtr() is only
    valid in Python 2.

    '''
    arr = cnp.PyArray_SimpleNewFromData(nd, dims, typenum, data)
    cdef _dealloc_shim dd = _dealloc_shim()
    dd._data = data
    cnp.set_array_base(arr, dd)
    return arr
