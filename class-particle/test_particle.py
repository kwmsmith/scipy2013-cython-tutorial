from particle import Particle

p = Particle()
assert(p.mass == 0.0)
assert(p.charge == 0.0)
assert(p.momentum == (0.0,)*3)
assert(p.speed == 0.0)

p.velocity = [3,4,0]
assert(p.speed == 5)

p.mass = 2.0
assert(p.momentum == (6,8,0))
