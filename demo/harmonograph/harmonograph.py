import numpy as np
from numpy import exp, sin, pi
from numpy.random import uniform

def random_frequencies():
    fs = [uniform(10,10.5) for _ in range(4)]
    fs[1] = fs[3]
    return fs

def random_phases():
    phs = [uniform(0, 2*pi) for _ in range(4)]
    return phs

def random_decay():
    return [uniform(0.025, .03) for _ in range(4)]

def compute(t, amps=None, fs=None, phs=None, ds=None):
    amps = amps or [1.0] * 4
    fs = fs or random_frequencies()
    phs = phs or random_phases()
    ds = ds or random_decay()
    args = amps + ds + fs + phs + [t]
    return xyt(*args)

def dosc(a, d, f, p, t):
    """
    d -- damping parameter.  Typically 0 < d < 1.
    f -- frequency.
    p -- phase, 0 <= p <= 2 * pi.
    t -- time.
    """
    return a * exp(-d*t) * sin(f * t + p)

def xyt(ax1, ax2, ay1, ay2, dx1, dx2, dy1, dy2, fx1, fx2, fy1, fy2, px1, px2, py1, py2, t):
    x = dosc(ax1, dx1, fx1, px1, t) + dosc(ax2, dx2, fx2, px2, t)
    y = dosc(ay1, dy1, fy1, py1, t) + dosc(ay2, dy2, fy2, py2, t)
    return x, y

def main(N):
    import matplotlib
    matplotlib.use('MacOSX')
    from matplotlib import pyplot as plt
    t = np.linspace(0, 40, 5000)
    for _ in range(N):
        x, y = compute(t)
        fname = 'harmonograph_{:03d}.png'.format(_)
        plt.plot(x, y)
        plt.savefig(fname)
        plt.clf()
        
if __name__ == '__main__':
    main(10)

# def soln0(L0, L1, p0y, p1x):
    # pmag2 = p0y**2 + p1x**2
    # L2diff = L0**2 - L1**2
    
    # Ldiff2 = (L0 - L1)**2
    # Lsum2 = (L0 + L1)**2
    
    # zx = (L2diff/2 - p0y**2/2 + p0y*(p0y*(pmag2 - L2diff) - 
        # sqrt(p1x**2*(pmag2 - Ldiff2)*(Lsum2 - pmag2)))/(2*pmag2) + p1x**2/2)/p1x
    # zy = (p0y*(pmag2 - L2diff)/2 - sqrt(p1x**2*(pmag2 - Ldiff2)*(Lsum2 - pmag2))/2)/pmag2
    # return zx, zy

# def soln1(L0, L1, p0y, p1x):
    # pmag2 = p0y**2 + p1x**2
    # L2diff = L0**2 - L1**2
    
    # Ldiff2 = (L0 - L1)**2
    # Lsum2 = (L0 + L1)**2
    
    # zx = (L2diff/2 - p0y**2/2 + p0y*(p0y*(pmag2 - L2diff) + 
        # sqrt(p1x**2*(pmag2 - Ldiff2)*(Lsum2 - pmag2)))/(2*pmag2) + p1x**2/2)/p1x
    # zy = (p0y*(pmag2 - L2diff)/2 + sqrt(p1x**2*(pmag2 - Ldiff2)*(Lsum2 - pmag2))/2)/pmag2
    # return zx, zy

# soln = [
        # {
            # zx: (L0**2/2 - L1**2/2 - p0y**2/2 + p0y*(p0y*(-L0**2 + L1**2 + p0y**2 + p1x**2) - sqrt(p1x**2*(-L0**2 + 2*L0*L1 - L1**2 + p0y**2 + p1x**2)*(L0**2 + 2*L0*L1 + L1**2 - p0y**2 - p1x**2)))/(2*(p0y**2 + p1x**2)) + p1x**2/2)/p1x,
        # zy: (p0y*(-L0**2 + L1**2 + p0y**2 + p1x**2)/2 - sqrt(p1x**2*(-L0**2 + 2*L0*L1 - L1**2 + p0y**2 + p1x**2)*(L0**2 + 2*L0*L1 + L1**2 - p0y**2 - p1x**2))/2)/(p0y**2 + p1x**2)},

       # {
           # zx: (L0**2/2 - L1**2/2 - p0y**2/2 + p0y*(p0y*(-L0**2 + L1**2 + p0y**2 + p1x**2) + sqrt(p1x**2*(-L0**2 + 2*L0*L1 - L1**2 + p0y**2 + p1x**2)*(L0**2 + 2*L0*L1 + L1**2 - p0y**2 - p1x**2)))/(2*(p0y**2 + p1x**2)) + p1x**2/2)/p1x,
           # zy: (p0y*(-L0**2 + L1**2 + p0y**2 + p1x**2)/2 + sqrt(p1x**2*(-L0**2 + 2*L0*L1 - L1**2 + p0y**2 + p1x**2)*(L0**2 + 2*L0*L1 + L1**2 - p0y**2 - p1x**2))/2)/(p0y**2 + p1x**2)}]
