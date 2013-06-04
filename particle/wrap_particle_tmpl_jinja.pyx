cimport cython
from libcpp.vector cimport vector
from cython.operator cimport dereference as deref

cdef extern from "particle_tmpl.h":

    cdef cppclass _Particle "Particle"[T]:
        _Particle()
        _Particle(T, T, T, T, T, T, T, T)
        const T get_speed()
        const T get_x()


    const double _norm2 "norm2"(double x, double y, double z)
    double _rms_speeds "rms_speeds"(vector[const _Particle[double]*] *particles)

    const float _norm2 "norm2"(float x, float y, float z)
    float _rms_speeds "rms_speeds"(vector[const _Particle[float]*] *particles)


# depend on type conversion rules to handle this case...
def norm2(double x, double y, double z):
    cdef double pn = _norm2(x, y, z)
    return pn


cdef class Particle_double:
    template_type = "double"
    cdef _Particle[double] *_thisptr
    def __cinit__(self, x, y, z, vx, vy, vz, mass, charge):
        self._thisptr = new _Particle[double](x, y, z, vx, vy, vz, mass, charge)
    cpdef double get_x(self):
        return self._thisptr.get_x()
    def __dealloc__(self):
        del self._thisptr

cpdef double rms_speeds_double(particles) except *:

    cdef:
        vector[const _Particle[double] *] vparticles
        _Particle[double] *part

    for particle in particles:
        if not isinstance(particle, Particle_double):
            raise TypeError("object %r is not an instance of Particle." % particle)
        part = (<Particle_double>particle)._thisptr
        vparticles.push_back(part)

    return _rms_speeds(&vparticles)

cdef class Particle_float:
    template_type = "float"
    cdef _Particle[float] *_thisptr
    def __cinit__(self, x, y, z, vx, vy, vz, mass, charge):
        self._thisptr = new _Particle[float](x, y, z, vx, vy, vz, mass, charge)
    cpdef float get_x(self):
        return self._thisptr.get_x()
    def __dealloc__(self):
        del self._thisptr

cpdef float rms_speeds_float(particles) except *:

    cdef:
        vector[const _Particle[float] *] vparticles
        _Particle[float] *part

    for particle in particles:
        if not isinstance(particle, Particle_float):
            raise TypeError("object %r is not an instance of Particle." % particle)
        part = (<Particle_float>particle)._thisptr
        vparticles.push_back(part)

    return _rms_speeds(&vparticles)


def Particle(*args, dtype='f'):
    type_dict = {
            'd': Particle_double,
            'f': Particle_float,
            }
    return type_dict[dtype](*args)

def rms_speeds(particles):
    type_dict = {
            'double': rms_speeds_double,
            'float': rms_speeds_float,
            }
    tp = particles[0].template_type
    return type_dict[tp](particles)