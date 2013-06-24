#ifndef _PARTICLE_H_
#define _PARTICLE_H_

#include <cmath>
#include <vector>

    template<typename T>
inline const T norm2(const T x, const T y, const T z)
{
    return sqrt(x * x + y * y + z * z);
}

template <typename T>
class Particle 
{
    public:

        Particle() : _x(0), _y(0), _z(0),
        _vx(0), _vy(0), _vz(0),
        _mass(0), _charge(0) {};

        Particle(T x, T y, T z,
                T vx, T vy, T vz,
                T mass, T charge) :
            _x(x), _y(y), _z(z),
            _vx(vx), _vy(vy), _vz(vz),
            _mass(mass), _charge(charge) {};

        const T get_speed() const {
            return norm2(_vx, _vy, _vz);
        }

        const T& get_x() const {
            return _x;
        }

    private:
        T _x, _y, _z;
        T _vx, _vy, _vz;
        T _mass;
        T _charge;
};

template <typename T>
T rms_speeds(std::vector<const Particle<T>*> *particles)
{
    T sum_speeds_sq = 0;
    typedef typename std::vector<const Particle<T> * >::const_iterator ParticleIter;
    
    for (ParticleIter it=particles->begin(); it != particles->end(); ++it) {
        sum_speeds_sq += (*it)->get_speed() * (*it)->get_speed();
    }
    return sqrt(sum_speeds_sq / particles->size());
}

#endif
