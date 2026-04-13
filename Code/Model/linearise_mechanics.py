from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Tuple

import numpy as np


@dataclass
class Params:
    """
    Mechanical parameters in SI units.
     Convention:
      - x is along incline, positive downhill
      - Magnetic force acts downhill toward x = delta
    """
    m: float = 0.462
    g: float = 9.81
    phi: float = math.radians(41.0)  
    k: float = 1885.0
    b: float = 10.4
    d: float = 0.42
    delta: float = 0.65
    c: float = 6.811e-3 #converted g -> kg
    eps: float = 1e-9              


def compute_i0(x0: float, p: Params) -> float:
    gap = p.delta - x0
    if gap <= 0:
        raise ValueError(f"x0 must be < delta. Got x0={x0}, delta={p.delta}")

    i0_sq = (p.k * (x0 - p.d) - p.m * p.g * math.sin(p.phi)) * (gap ** 2) / p.c

    if i0_sq < 0:
        raise ValueError(
            "No real equilibrium current for this x0 with the chosen force directions.\n"
            f"Computed i0^2 = {i0_sq:.6g} < 0.\n"
            "Try x0 > d (spring stretched) and ensure x0 < delta."
        )

    return math.sqrt(i0_sq)


def linearise_mechanics(
    x0: float,
    i0: float | None = None,
    p: Params | None = None,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    if p is None:
        p = Params()

    if i0 is None:
        i0 = compute_i0(x0, p)

    gap = max(p.delta - x0, p.eps)

    gain = 5.0 / (7.0 * p.m)

    #Partial derivatives at operating point (x0, v0=0, i0)
    a_v = gain * (-p.b)

    a_i = gain * (p.c * (2.0 * i0) / (gap ** 2))

    a_x = gain * (-p.k + p.c * (i0 ** 2) * (2.0 / (gap ** 3)))

    A = np.array([[0.0, 1.0],
                  [a_x, a_v]], dtype=float)

    B = np.array([[0.0],
                  [a_i]], dtype=float)

    C = np.array([[1.0, 0.0]], dtype=float)
    D = np.array([[0.0]], dtype=float)

    return A, B, C, D


if __name__ == "__main__":
    p = Params()
    x0 = 0.43
    i0 = compute_i0(x0, p)
    A, B, C, D = linearise_mechanics(x0=x0, i0=i0, p=p)

    print(f"x0 = {x0:.3f} m")
    print(f"i0 = {i0:.4f} A")
    print("A =\n", A)
    print("B =\n", B)
    print("C =\n", C)
    print("D =\n", D)
