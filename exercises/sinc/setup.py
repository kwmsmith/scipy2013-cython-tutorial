from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

exts = [
        Extension("sinc_kernel", ["sinc_kernel.pyx"]),
        Extension("sinc_solution", ["sinc_solution.pyx"]),
        ]

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = exts,
)
