"""
This script simulates the complete ball on incline system

State vector:
    x1 = x       ball position along incline [m]  (positive downhill)
    x2 = v       ball velocity [m/s]
    x3 = i       circuit current [A]
    x4 = x_m     sensor output (measured position) [m]

Input:
    vin          applied voltage [V]

Output:
    y = x4       sensor measurement

All four states are integrated together by solve_ivp.
"""

from __future__ import annotations
from dataclasses import dataclass
import math

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


# ---------------------------------------------------------------------------
# system parameters
# ---------------------------------------------------------------------------

@dataclass
class SystemParams:

    # Mechanical
    m:     float = 0.462               # ball mass [kg]
    g:     float = 9.81                # gravitational acceleration [m/s^2]
    phi:   float = math.radians(41.0)  # incline angle [rad]
    k:     float = 1885.0              # spring stiffness [N/m]
    b:     float = 10.4                # viscous damping coefficient [N*s/m]
    d:     float = 0.42                # spring natural length position [m]
    r:     float = 0.123               # ball radius [m]
    c:     float = 6.811e-3            # magnetic force constant [m^3*kg/(A^2*s^2)]
    delta: float = 0.65                # electromagnet centre position [m]

    # Electrical
    R:     float = 2200.0              # resistance [Ohm]
    L0:    float = 0.125               # nominal inductance [H]
    L1:    float = 0.0241              # inductance coefficient [H]
    alpha: float = 1.2                 # inductance decay constant [m^-1]

    # Sensor
    tau_m: float = 0.03                # sensor time constant [s]
    Km:    float = 1.0                 # sensor gain

    # Numerical safety
    eps:   float = 1e-6                # prevents division by zero if x -> delta

    def __getitem__(self, key: str):
        return getattr(self, key)

# ---------------------------------------------------------------------------
# Individual subsystem functions
# ---------------------------------------------------------------------------

def inductance(x, p):
    return p["L0"] + p["L1"] * np.exp(-p["alpha"] * (p["delta"] - x))


def mech_accel(x1: float, x2: float, x3: float, p: SystemParams) -> float:
    """
    Mechanical acceleration along the incline (x2_dot = ẍ).

    Effective mass accounts for rolling inertia of solid sphere:
        m_eff = (7/5) * m   (from I = 2/5 * m * r^2 and rolling constraint)

    Forces (positive = downhill):
        Fg   = m * g * sin(phi)          gravity component
        Fs   = -k * (x1 - d)            spring  (restoring when x1 > d)
        Fd   = -b * x2                   viscous damper
        Fmag = c * x3^2 / (delta-x1)^2  electromagnetic attraction (downhill)
    """
    m_eff = (7.0 / 5.0) * p.m
    gap   = max(p.delta - x1, p.eps)  # distance to electromagnet, clamped > 0

    Fg   =  p.m * p.g * math.sin(p.phi)
    Fs   = -p.k * (x1 - p.d)
    Fd   = -p.b * x2
    Fmag =  p.c * x3**2 / gap**2

    return (Fg + Fs + Fd + Fmag) / m_eff


def elec_deriv(x1: float, x3: float, vin: float, p: SystemParams) -> float:
    """
    Rate of change of current (x3_dot = di/dt).

    Derived from KVL with position-dependent inductance:
        V = R*i + d(L*i)/dt

    Assumption A1: the term i*(dL/dt) is neglected (valid near equilibrium
    where velocity x2 ≈ 0, making dL/dt = (dL/dx1)*x2 ≈ 0).
    This gives the simplified form:
        di/dt = (V - R*i) / L(x1)

    See electrical_sensor_derivation.md for full justification.
    """
    L = inductance(x1, p)
    return (vin - p.R * x3) / L


def sensor_deriv(x1: float, x4: float, p: SystemParams) -> float:
    """
    Rate of change of sensor output (x4_dot = dx_m/dt).

    The sensor is a first-order system with time constant tau_m:
        tau_m * dx_m/dt + x_m = Km * x1

    Rearranging:
        dx_m/dt = (Km * x1 - x4) / tau_m

    This is the CORRECTED implementation. The previous sensor.py used a
    static gain y = Km*x, which is only valid at steady state and ignores
    the 30 ms lag during transients.
    """
    return (p.Km * x1 - x4) / p.tau_m


# ---------------------------------------------------------------------------
# Full 4-state ODE right-hand side
# ---------------------------------------------------------------------------

def full_system_rhs(
    t: float,
    state: list[float],
    vin_func,           # callable: vin_func(t) -> voltage [V]
    p: SystemParams,
) -> list[float]:
    """
    Full nonlinear system RHS for use with scipy.integrate.solve_ivp.

    Parameters
    ----------
    t        : current time [s]
    state    : [x1, x2, x3, x4]
    vin_func : function returning the input voltage at time t
    p        : SystemParams instance

    Returns
    -------
    [dx1/dt, dx2/dt, dx3/dt, dx4/dt]
    """
    x1, x2, x3, x4 = state
    vin = vin_func(t)

    dx1 = x2
    dx2 = mech_accel(x1, x2, x3, p)
    dx3 = elec_deriv(x1, x3, vin, p)
    dx4 = sensor_deriv(x1, x4, p)

    return [dx1, dx2, dx3, dx4]


# ---------------------------------------------------------------------------
# Open-loop simulation
# ---------------------------------------------------------------------------

def run_open_loop(
    p: SystemParams | None = None,
    x1_0: float = 0.5,     # initial ball position [m]
    x2_0: float = 0.0,      # initial velocity [m/s]
    x3_0: float = 22.1,     # initial current [A]  (equilibrium value at x0=0.50 m)
    x4_0: float = 0.5,     # initial sensor output [m]  (= x1_0 at steady state)
    t_end:float = 0.5,      # simulation duration [s]
    vin_func=None,          # input voltage function; defaults to equilibrium V0
) -> None:
    """
    Runs and plots an open-loop simulation of the full nonlinear system.
    """
    if p is None:
        p = SystemParams()

    # Default input: equilibrium voltage V0 = R * i0
    # At steady state di/dt = 0 => V = R*i, so V0 = R * x3_0
    if vin_func is None:
        V0 = p.R * x3_0
        vin_func = lambda t: V0

    t_span = (0.0, t_end)
    t_eval = np.linspace(0.0, t_end, 2000)
    y0     = [x1_0, x2_0, x3_0, x4_0]

    sol = solve_ivp(
        fun=lambda t, y: full_system_rhs(t, y, vin_func, p),
        t_span=t_span,
        y0=y0,
        t_eval=t_eval,
        method="RK45",
        rtol=1e-8,
        atol=1e-10,
    )

    if not sol.success:
        raise RuntimeError(f"Simulation failed: {sol.message}")

    x1, x2, x3, x4 = sol.y
    vin_vals = np.array([vin_func(t) for t in sol.t])

    # --- Plot ---
    fig, axes = plt.subplots(5, 1, figsize=(10, 12), sharex=True)

    axes[0].plot(sol.t, x1, label="x₁ - ball position")
    axes[0].set_ylabel("x₁ [m]")
    axes[0].set_title("Open-loop simulation: full nonlinear system")
    axes[0].legend(loc='upper left'); axes[0].grid(True)

    axes[1].plot(sol.t, x2, label="x₂ - velocity", color="tab:orange")
    axes[1].set_ylabel("x₂ [m/s]")
    axes[1].legend(loc='upper left'); axes[1].grid(True)

    axes[2].plot(sol.t, x3, label="x₃ - current", color="tab:green")
    axes[2].set_ylabel("x₃ [A]")
    axes[2].legend(loc='upper left'); axes[2].grid(True)

    axes[3].plot(sol.t, x4, label="x₄ - sensor output", color="tab:red")
    axes[3].plot(sol.t, x1, "--", alpha=0.4, label="x₁ (true)", color="tab:blue")
    axes[3].set_ylabel("x₄ [m]")
    axes[3].legend(loc='upper left'); axes[3].grid(True)

    axes[4].plot(sol.t, vin_vals, label="Vᵢₙ - input voltage", color="tab:purple")
    axes[4].set_ylabel("Vᵢₙ [V]")
    axes[4].set_xlabel("Time [s]")
    axes[4].legend(loc='upper left'); axes[4].grid(True)

    plt.tight_layout()
    plt.savefig("open_loop_simulation.png", dpi=150)
    plt.show()
    print("Plot saved to open_loop_simulation.png")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    p = SystemParams()

    print("System parameters:")
    print(f"  Operating point: x0 = 0.5 m")
    print(f"  Equilibrium current: i0 = {p.R * 22.1:.1f} V -> i0 = 22.1 A")
    print(f"  Equilibrium voltage: V0 = R * i0 = {p.R * 22.1:.1f} V")
    print(f"  Sensor time constant: tau_m = {p.tau_m * 1000:.0f} ms")
    print()

    run_open_loop(p=p)