def sensor_deriv(x1: float, x4: float, p) -> float:
    """
    x1  : true ball position [m]
    x4  : current sensor output / measured position [m]
    p   : parameters object with attributes tau_m and Km
    """
    return (p.Km * x1 - x4) / p.tau_m