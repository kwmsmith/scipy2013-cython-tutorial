import numpy as np
from numpy.random import uniform
from scipy.integrate import odeint

def f(y, t, l0, l1, g):
    from math import sin, cos
    th0, th1, th0dot, th1dot = y
    D = l0 + l1 * cos(th1)
    th0ddot = 1. / D * (2 * l1 * sin(th1) * th1dot * th0dot - g * sin(th0))
    th1ddot = -1. / l1 * sin(th1) * (D * th0dot * th0dot + g * cos(th0))
    return [th0dot, th1dot, th0ddot, th1ddot]

def curve_in_space(th0, th1, l0, l1):
    # th0 determines the mass' y position.
    # th1 determines the mass' x position.
    D = l0 + l1 * np.cos(th1)
    ys = D * np.sin(th0)
    xs = l0 * np.sin(th1)
    return xs, ys


# bounds = [(-3.0, 3.0),
          # (-3.0, 3.0),
          # (-1.0, 1.0),
          # (-1.0, 1.0),
          # ]
          
bounds = [(-1e-2, 1e-2),
          (-1e-2, 1e-2),
          (-1.0, 1.0),
          (-1.0, 1.0),
          ]

def get_random_init_conds(bounds):
    return [uniform(*b) for b in bounds]

def make_plot(soln, l0, l1, fname):
    import matplotlib
    matplotlib.use('png')
    import matplotlib.pyplot as plt
    cis = curve_in_space(soln[:,0], soln[:,1], l0, l1)
    plt.plot(*cis)
    plt.savefig(fname)
    plt.close('all')
    
def main(N):
    t = np.linspace(0, 1000., 5000)
    l0 = 1.0
    g = 1.0
    for _ in range(N):
        print "{} / {}".format(_+1, N)
        ics = get_random_init_conds(bounds)
        l1, = get_random_init_conds([(0.01, 2.0)])
        soln = odeint(f, ics, t, args=(l0, l1, g))
        fname = "blackburn_pendulum_{}_{}_{}_{}_{}.png".format(*(ics + [l1]))
        make_plot(soln, l0, l1, fname)
    
if __name__ == '__main__':
    main(100)
