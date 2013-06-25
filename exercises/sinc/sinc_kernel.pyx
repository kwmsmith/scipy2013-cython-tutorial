from libc.math cimport sin

cdef double sinc_kernel(double x):
    '''
    sinc_kernel(x) -> sin(x) / x
    ...
    '''
    cdef double out
    if -0.01 < x < 0.01:
        out = 1.0
    else:
        out = sin(x) / x
    return out
