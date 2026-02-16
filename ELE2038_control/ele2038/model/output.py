import numpy as np

def g(x, u, p):
    x = np.asarray(x).reshape(-1)
    return float(x[3])  # sensor output