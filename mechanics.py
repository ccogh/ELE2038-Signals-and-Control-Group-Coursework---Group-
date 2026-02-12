from __future__ import annotations
from dataclasses import dataclass
import math


@dataclass
class MechParams:
    m: float    #mass [kg]
    g: float    #gravity [m/s^2]
    phi: float  #incline angle [rad]
    k: float    #spring stiffness [N/m]
    b: float    #viscous damping [N*s/m]
    d: float    #spring natural length position [m]
    c: float    #magnetic force constant
    delta: float    #magnet centre position [m]
    r: float    #ball radius [m]
    eps: float = 1e-6   #small number to avoid division by zero


def accel(x: float, v: float, i: float, p: MechParams) -> float:
    """
    Acceleration for a rolling solid sphere (ball) on an incline.

    Convention:
      - x is along the incline, positive downhill.
      - Magnetic force pulls toward x = delta.
      - Frame of reference (FOR) CCW -> positive.

    """
    m_eff = (7.0 / 5.0) * p.m

    #Forces along incline (downhill -> positive)
    Fg = p.m * p.g * math.sin(p.phi)
    Fs = -p.k * (x - p.d)
    Fd = -p.b * v

    gap = max(p.delta - x, p.eps)  #Prevents system 'blowing up' if x -> delta
    Fmag = p.c * (i ** 2) / (gap ** 2)

    return (Fg + Fs + Fd + Fmag) / m_eff


def mech_rhs(t: float, state: tuple[float, float], i: float, p: MechParams) -> tuple[float, float]:
    "Returns (x_dot, v_dot) for state = (x, v)."
    x, v = state
    return v, accel(x, v, i, p)