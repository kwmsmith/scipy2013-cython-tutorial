import numpy as np
import timeit
import pyximport
import sys

setup_args = {}
if sys.platform == 'win32':
    setup_args={'options': {'build_ext': {'compiler': 'mingw32'}}}
pyximport.install(setup_args=setup_args)

import sinc_python
import sinc_kernel
import sinc_solution

sinc_py = np.vectorize(sinc_python.sinc_kernel)
sinc_cy = np.vectorize(sinc_kernel.sinc_kernel)
sinc_cy_soln = np.vectorize(sinc_solution.sinc_kernel)

x = np.linspace(-5*np.pi, 5*np.pi, 1000)

print "Python time:", timeit.timeit('sinc_py(x)', 'from __main__ import sinc_py,x', number=100)
print "Cython time:", timeit.timeit('sinc_cy(x)', 'from __main__ import sinc_cy,x', number=100)
print "Solution time:", timeit.timeit('sinc_cy_soln(x)', 'from __main__ import sinc_cy_soln,x', number=100)
