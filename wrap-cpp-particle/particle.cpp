#include "particle.h"
#include <vector>

float rms_speeds(std::vector<const Particle*> *particles)
{
    float sum_speeds_sq = 0;
    typedef std::vector<const Particle*>::const_iterator ParticleIter;
    
    for (ParticleIter it=particles->begin(); it != particles->end(); ++it) {
        sum_speeds_sq += (*it)->get_speed() * (*it)->get_speed();
    }
    return sqrt(sum_speeds_sq / particles->size());
}
