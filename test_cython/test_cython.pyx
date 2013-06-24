def testcython(int n):
    return 3.1415**n

print testcython(10)

from libc.string cimport strlen

def get_len(char *msg):
    return strlen(msg)

print get_len("asdfasfd\0asdfasfd")

import numpy as np

def testmemview(double[:,::1] mv):
    ''' Tests roundtrip: python object -> cython typed memoryview -> python object '''
    print np.sum(mv)

from numpy import ones
testmemview(ones((10, 10)))
