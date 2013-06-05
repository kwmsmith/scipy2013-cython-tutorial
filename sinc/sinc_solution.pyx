from libc.math cimport sin

cpdef float sinc_kernel(float x):
    if -0.01 < x < 0.01:
        return 1.0
    return sin(x) / x

# --- Everything below is for demo purposes ----------------------------------

import numpy as np
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def sinc_cython(float[::1] a):
    '''
    Works for 1D arrays only; not as general as np.vectorize()
    
    '''
    cdef:
        float[::1] result = np.empty_like(a)
        int i, n

    n = a.shape[0]
    for i in range(n):
        result[i] = sinc_kernel(a[i])
    return result
