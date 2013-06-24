from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

# ext = Extension("wrap_particle_tmpl", ["wrap_particle_tmpl.pyx", "particle_tmpl.cpp"], language="c++")
ext = Extension("wrap_particle_tmpl", ["wrap_particle_tmpl_jinja.pyx", "particle_tmpl.cpp"], language="c++")

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [ext],
)
