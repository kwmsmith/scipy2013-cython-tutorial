from libcpp.vector cimport vector
from cython.operator cimport dereference as deref

cdef extern from "particle.h":
    
    const float _norm2 "norm2"(float x, float y, float z)

    cdef cppclass _Particle "Particle":
        _Particle()
        _Particle(float, float, float,
                 float, float, float,
                 float, float)
        const float get_speed()
        const float get_x()
    
    float _rms_speeds "rms_speeds"(vector[const _Particle*] *particles)
        
def norm2(float x, float y, float z):
    cdef float pn = _norm2(x, y, z)
    return pn

cdef class Particle:
    cdef _Particle *_thisptr
    def __cinit__(self, x, y, z, vx, vy, vz, mass, charge):
        self._thisptr = new _Particle(x, y, z, vx, vy, vz, mass, charge)
    cpdef float get_x(self):
        return self._thisptr.get_x()
    def __dealloc__(self):
        del self._thisptr
        
cpdef float rms_speeds(particles) except *:
    
    cdef:
        vector[const _Particle *] vparticles
        _Particle *part

    for particle in particles:
        if not isinstance(particle, Particle):
            raise TypeError("object %r is not an instance of Particle." % particle)
        part = (<Particle>particle)._thisptr
        vparticles.push_back(part)
        
    return _rms_speeds(&vparticles)

if __name__ == '__main__':
    import numpy as np
    assert np.allclose(norm2(1, 2, 3), np.sqrt(14.0))
