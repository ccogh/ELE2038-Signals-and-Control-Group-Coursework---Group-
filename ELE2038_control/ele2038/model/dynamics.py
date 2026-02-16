import numpy as np
from ele2038.model.mechanics import mech_rhs

from ele2038.model.electrical import di_dt
from ele2038.model.sensor import sensor_dy_dt

def f(t, x, u, p):
    """
    Full nonlinear dynamics for solve_ivp.

    State ordering (must stay consistent):
      x[0]=position, x[1]=velocity, x[2]=current, x[3]=sensor output

    Input:
      u = vin (voltage)

    Params:
      p["mech"] = MechParams(...)
      p["elec"] = dict(...)
      p["sens"] = dict with Km, tau_m
    """
    x = np.asarray(x).reshape(-1)
    if x.shape[0] != 4:
        raise ValueError(f"Expected state dimension 4, got {x.shape[0]}")

    pos, vel, current, y = x

    # Mechanical
    dpos, dvel = mech_rhs(t, (pos, vel), current, p["mech"])

    # Electrical
    dcurrent = di_dt(current, u, pos, vel, p["elec"])

    # Sensor (first-order)
    dy = sensor_dy_dt(pos, y, p["sens"])

    return np.array([dpos, dvel, dcurrent, dy], dtype=float)