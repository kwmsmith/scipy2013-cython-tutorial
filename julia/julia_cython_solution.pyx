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
from libc.stdlib cimport free
from cpython.cobject cimport PyCObject_FromVoidPtr
cimport numpy as cnp

# --- Local Ctypedefs --------------------------------------------------------
# Necessary to declare these typedefs here (not in the cdef extern block).
# NOTE: Make sure these stay in sync with the _julia_ext.h header typedefs!!

ctypedef float         real_t
ctypedef cnp.uint32_t  uint_t
ctypedef cnp.int32_t   int_t

# #-----------------------------------------------------------------------------
# # External declarations
# #-----------------------------------------------------------------------------
# cdef extern from "_julia_ext.h" nogil:

    # unsigned int ext_julia_kernel "julia_kernel"(cpx_t, cpx_t, 
                                                 # real_t, real_t)
    # unsigned int *ext_compute_julia "compute_julia"(cpx_t, unsigned int,
                                               # real_t, real_t)

# Necessary to call `np.import_array()` before calling functions from the NumPy
# C-API.

#-----------------------------------------------------------------------------
# Cython functions
#-----------------------------------------------------------------------------
def compute_julia_no_opt(real_t cr, real_t ci,
                         unsigned int N,
                         real_t bound=1.5,
                         real_t lim=1000.):
    ''' 
    Cythonized version of a pure Python implementation of the compute_julia()
    function.  It uses numpy arrays, but does not use any extra syntax to speed
    things up beyond simple type declarations.

    '''
    
    cdef:
        int i, j
        real_t x, y
        
    julia = np.empty((N, N), dtype=np.uint32)
    grid = np.linspace(-bound, bound, N)
    t0 = time()
    for i in range(N):
        x = grid[i]
        for j in range(N):
            y = grid[j]
            julia[i,j] = kernel(x, y, cr, ci, lim)
    return julia, time() - t0

cdef inline real_t abs_sq(real_t zr, real_t zi) nogil:
    return zr * zr + zi * zi

cpdef uint_t kernel(real_t zr, real_t zi,
                    real_t cr, real_t ci,
                    real_t lim,
                    real_t cutoff=1e6) nogil:
    ''' Cython implementation of the kernel computation.

    This is implemented so that no C-API calls are made inside the function
    body.  Even still, there is some overhead as compared with a pure C
    implementation.
    '''
    cdef:
        uint_t count = 0
        real_t lim_sq = lim * lim
    while abs_sq(zr, zi) < lim_sq and count < cutoff:
        zr, zi = zr * zr - zi * zi + cr, 2 * zr * zi + ci
        # z = z * z * z + c
        count += 1
    return count

@cython.boundscheck(False)
@cython.wraparound(False)
def compute_julia_opt(real_t cr, real_t ci,
                       uint_t N,
                       real_t bound=1.5,
                       real_t lim=1000.,
                       real_t cutoff=1e6):
    '''
    Cython `compute_julia()` implementation with Numpy array buffer
    declarations and appropriate compiler directives.  The body of this
    function is nearly identical to the `compute_julia_no_opt()` function.

    '''

    cdef:
        uint_t[:,::1] julia 
        real_t[::1] grid
        int_t i, j
        real_t x

    julia = np.empty((N, N), dtype=np.uint32)
    grid = np.asarray(np.linspace(-bound, bound, N), dtype=np.float32)
    t0 = time()
    with nogil:
        for i in prange(N):
            x = grid[i]
            for j in range(N):
                julia[i,j] = kernel(x, grid[j], cr, ci, lim, cutoff)
    return julia, time() - t0

# def compute_julia_ext(cpx_t c,
                       # unsigned int N,
                       # real_t bound=1.5,
                       # real_t lim=1000.):
    # '''
    # Call an externally implemented version of `compute_julia()` and wrap the
    # resulting C array in a NumPy array.

    # '''
    # t0 = time()
    # cdef unsigned int *julia = ext_compute_julia(c, N, bound, lim)
    # cdef cnp.npy_intp dims[2]
    # dims[0] = N; dims[1] = N
    # arr = new_array_owns_data_cython(2, dims, cnp.NPY_UINT, <void*>julia)
    # return arr, time() - t0


# cdef void local_free(void *data):
    # ''' Wraps `free()` from C's stdlib with some output to indicate that it's
    # been called.
    # '''
    # free(data)

# cdef object new_array_owns_data(int nd,
                                # cnp.npy_intp *dims,
                                # int typenum,
                                # void *data):
    # ''' Creates a Numpy array with data from the `data` buffer.  Sets the array
    # base appropriately using `PyCObject_FromVoidPtr()` to ensure that the data
    # gets cleaned up when the Numpy array object is garbage collected.

    # '''
    # arr = cnp.PyArray_SimpleNewFromData(nd, dims, typenum, data)
    # cnp.set_array_base(arr, PyCObject_FromVoidPtr(data, local_free))
    # return arr

# cdef class _dealloc_shim:
    # ''' Deallocation shim class that exists simply to free() the _data pointer.
    # '''
    # cdef void *_data

    # def __cinit__(self):
        # self._data = NULL

    # def __dealloc__(self):
        # if self._data:
            # free(self._data)
        # self._data = NULL

# cdef object new_array_owns_data_cython(int nd,
                                       # cnp.npy_intp *dims,
                                       # int typenum,
                                       # void *data):
    # ''' Same as `new_array_owns_data()`, but uses a `_dealloc_shim` instance
    # rather than `PyCObject_FromVoidPtr()`.  This solution is usable from all
    # Python versions (Python 2 and 3), whereas PyCObject_FromVoidPtr() is only
    # valid in Python 2.

    # '''
    # arr = cnp.PyArray_SimpleNewFromData(nd, dims, typenum, data)
    # cdef _dealloc_shim dd = _dealloc_shim()
    # dd._data = data
    # cnp.set_array_base(arr, dd)
    # return arr
