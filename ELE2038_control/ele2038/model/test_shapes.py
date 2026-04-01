import numpy as np
from ele2038.model.dynamics import f
from ele2038.model.output import g
from ele2038.model.mechanics import MechParams

def test_f_shape():
    mech = MechParams(m=1.0, g=9.81, phi=0.5, k=1.0, b=0.1, d=0.0, c=1e-3, delta=1.0, r=0.1)
    elec = {"R": 1.0, "L0": 1.0, "L1": 0.1, "alpha": 1.0, "delta": 1.0}
    sens = {"Km": 1.0, "tau_m": 0.03}
    p = {"mech": mech, "elec": elec, "sens": sens}

    x = np.zeros(4)
    u = 1.0
    dx = f(0.0, x, u, p)

    assert isinstance(dx, np.ndarray)
    assert dx.shape == (4,)

def test_g_scalar():
    mech = MechParams(m=1.0, g=9.81, phi=0.5, k=1.0, b=0.1, d=0.0, c=1e-3, delta=1.0, r=0.1)
    p = {"mech": mech, "elec": {}, "sens": {"Km": 1.0, "tau_m": 0.03}}
    y = g(np.zeros(4), 0.0, p)
    assert isinstance(y, float)