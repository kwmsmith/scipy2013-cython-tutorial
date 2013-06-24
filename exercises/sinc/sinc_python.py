from math import sin

def sinc_kernel(x):
    if -0.01 < x < 0.01:
        return 1.0
    return sin(x) / x
