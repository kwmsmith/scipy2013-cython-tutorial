from __future__ import print_function
import timeit
import numpy as np

import utils

def pysinc_kernel(x):
    if abs(x) < 0.01:
        return 1.0
    return np.sin(x) / x

def main(args):
    # make these global so we can use timeit...
    global pysinc, fast_sinc, arr, sinc_cython

    utils.compiler(args.setup)
    sinc_kernel = utils.importer(args.module, args.function)

    try:
        sinc_cython = utils.importer(args.module, 'sinc_cython')
    except ImportError:
        sinc_cython = None

    # Our input data
    arr = np.linspace(-5*np.pi, 5*np.pi, 10000).astype(np.float32)

    # vectorize the python and cython kernels.
    pysinc = np.vectorize(pysinc_kernel)
    fast_sinc = np.vectorize(sinc_kernel)

    # time the kernels
    ncalls = 20
    pytime = timeit.timeit('pysinc(arr)', 'from __main__ import pysinc, arr', number=ncalls)
    cython_time = timeit.timeit('fast_sinc(arr)', 'from __main__ import fast_sinc, arr', number=ncalls)
    if sinc_cython:
        all_cython_time = timeit.timeit('sinc_cython(arr)', 'from __main__ import sinc_cython,arr', number=ncalls)

    print("*" * 50)
    print("Number of repetitions: {}".format(ncalls))
    print( "array size           : {}".format(10000))
    print("Pure-python kernel   : {:.3f}s".format(pytime, ncalls))
    print("Cython kernel        : {:.3f}s".format(cython_time, ncalls))
    print("Speedup              : {:.1f}".format(pytime / cython_time))
    if sinc_cython:
        print("All Cython           : {:.3f}s".format(all_cython_time, ncalls))
        print("Speedup              : {:.1f}".format(cython_time / all_cython_time))
    print("*" * 50)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('module')
    parser.add_argument('-f', '--function', default='sinc_kernel')
    parser.add_argument('--setup', default='setup.py')
    main(parser.parse_args())
