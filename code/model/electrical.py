import numpy as np

def inductance(x, p):
    return p["L0"] + p["L1"] * np.exp(-p["alpha"] * (p["delta"] - x))


def di_dt(i, vin, x, v, p):
    L = inductance(x,p)
    return (vin - p["R"] * i) / L 
