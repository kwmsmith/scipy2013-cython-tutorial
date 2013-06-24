Vectorized Sinc with Cython
===========================

The goal of this exercise is to add type information to a `def` function to
speed it up with Cython.

The file `sinc_python.py` defines a simple function `sinc_kernel` that is
designed to be vectorized with numpy's `vectorize` decorator.  NumPy's
`vectorize` calls `sinc_kernel` on every element of the input array and
returns a new array of the results.  Since `sinc_python.sinc_kernel` is pure
Python, this will be slow.  We will be creating a Cython version of the same
kernel function to speed it up.

1. Run the `test_sinc.py` script which uses pyximport to compile and import
   the Cython source files for this exercise::

        $ python test_sinc.py
        Python time: 0.0476980209351
        Cython time: 0.0311279296875
        Solution time: 0.0171620845795

2. The `sinc_kernel.pyx` file contains an un-optimized version of the sinc
   kernel function.  Add type information so the `sinc_kernel` function takes
   a double and returns a double as a result.  Re-run the test script and see
   if there is any difference in the "Cython time".

3. The `sinc_kernel` function is calling the `sin()` function from Python's
   math library, which incurrs Python overhead for every call.  Change the 
   `from math import sin` to `from libc.math cimport sin` to use the `sin()`
   function from `math.h` directly.  Run the test and see if the "Cython time"
   improves.
