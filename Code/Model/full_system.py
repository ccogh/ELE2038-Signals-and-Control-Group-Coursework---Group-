"""
Nonlinear open-loop simulation of the complete ball-on-incline system.

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

from dataclasses import dataclass
import math

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from mechanics import mech_rhs
from electrical import di_dt
from sensor import sensor_deriv
from linearise_mechanics import Params, compute_i0


# operating point
X0 = 0.50   # ball position [m]


@dataclass
class SystemParams:

    # Mechanical
    m:     float = 0.462               # ball mass [kg]
    g:     float = 9.81                # gravitational acceleration [m/s^2]
    phi:   float = math.radians(41.0)  # incline angle [rad]
    k:     float = 1885.0              # spring stiffness [N/m]
    b:     float = 10.4                # viscous damping coefficient [N*s/m]
    d:     float = 0.42                # spring natural length position [m]
    c:     float = 6.811e-3            # magnetic force constant [m^3*kg/(A^2*s^2)]
    delta: float = 0.65                # electromagnet centre position [m]
    r:     float = 0.123               # ball radius [m]
    eps:   float = 1e-6                # prevents division by zero if x -> delta

    # Electrical
    R:     float = 2200.0              # resistance [Ohm]
    L0:    float = 0.125               # nominal inductance [H]
    L1:    float = 0.0241              # inductance coefficient [H]
    alpha: float = 1.2                 # inductance decay constant [m^-1]

    # Sensor
    tau_m: float = 0.03                # sensor time constant [s]
    Km:    float = 1.0                 # sensor gain

    def __getitem__(self, key):
        return getattr(self, key)

# current time [s], state [x1-4], input voltage at t, SystemParams
def full_system_rhs(t, state, vin_func, p):                       # returns: [dx1/dt, dx2/dt, dx3/dt, dx4/dt]
    x1, x2, x3, x4 = state
    vin = vin_func(t)

    dx1 = x2                                                      # position changes at rate of velocity
    _, dx2 = mech_rhs(t, (x1, x2), i = x3, p = p)                     # velocity changes at rate of acceleration (from mechanics.py)
    dx3 = di_dt(x3, vin, x1, x2, p)                               # current changes per circuit equation (from electrical.py)
    dx4 = sensor_deriv(x1, x4, p)                                 # sensor output chases true position with 30 ms lag (from sensor.py)

    return [dx1, dx2, dx3, dx4]

# t_end: simulation duration [s]
def run_open_loop(p, x1_0 = X0, x2_0 = 0.0, x3_0 = 22.1, x4_0 = X0, t_end = 0.5, vin_func = None):  # runs and plots an open-loop simulation of the full nonlinear system

    if vin_func is None:
        V0 = p.R * x3_0                                           # equilibrium voltage: at steady state di/dt = 0  = > V = R*i
        vin_func = lambda t: V0

    t_eval = np.linspace(0.0, t_end, 2000)
    y0 = [x1_0, x2_0, x3_0, x4_0]

    sol = solve_ivp(
        fun = lambda t, y: full_system_rhs(t, y, vin_func, p),
        t_span = (0.0, t_end),
        y0 = y0,
        t_eval = t_eval,
        rtol = 1e-8,
        atol = 1e-10,
    )

    if not sol.success:
        raise RuntimeError(f"Simulation failed: {sol.message}")

    x1, x2, x3, x4 = sol.y
    vin_vals = np.array([vin_func(t) for t in sol.t])

    fig, axes = plt.subplots(5, 1, figsize = (10, 12), sharex = True)

    axes[0].plot(sol.t, x1, label = "x1 - ball position")
    axes[0].set_ylabel("x1 [m]")
    axes[0].set_title("Open-loop simulation - full nonlinear system")
    axes[0].legend(loc = "upper left"); axes[0].grid(True)

    # velocity - expected to diverge in open loop due to RHP pole
    axes[1].plot(sol.t, x2, label = "x2 - velocity", color = "tab:orange")
    axes[1].set_ylabel("x2 [m/s]")
    axes[1].legend(loc = "upper left"); axes[1].grid(True)

    # current - stays approximately flat since voltage is held constant
    axes[2].plot(sol.t, x3, label = "x3 - current", color = "tab:green")
    axes[2].set_ylabel("x3 [A]")
    axes[2].legend(loc = "upper left"); axes[2].grid(True)

    # sensor output vs true position - shows 30 ms lag during transients
    axes[3].plot(sol.t, x4, label = "x4 - sensor output", color = "tab:red")
    axes[3].plot(sol.t, x1, "--", alpha = 0.4, label = "x1 (true)", color = "tab:blue")
    axes[3].set_ylabel("x4 [m]")
    axes[3].legend(loc = "upper left"); axes[3].grid(True)

    # input voltage - held constant at V0 throughout open-loop run
    axes[4].plot(sol.t, vin_vals, label = "Vin - input voltage", color = "tab:purple")
    axes[4].set_ylabel("Vin [V]")
    axes[4].set_xlabel("Time [s]")
    axes[4].legend(loc = "upper left"); axes[4].grid(True)

    plt.tight_layout()
    plt.savefig("open_loop_simulation.svg")
    plt.show()
    print("Plot saved to open_loop_simulation.svg")


if __name__ == "__main__":
    p  = SystemParams()
    i0 = compute_i0(X0, p)                                  # equilibrium current at operating point

    print("System parameters:")
    print(f"  Operating point:      x0    = {X0} m")
    print(f"  Equilibrium current:  i0    = {i0:.2f} A")
    print(f"  Equilibrium voltage:  V0    = {p.R * i0:.1f} V")
    print(f"  Sensor time constant: tau_m = {p.tau_m * 1000:.0f} ms")
    print()

    run_open_loop(p)