import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from ele2038.model.dynamics import f
from ele2038.model.output import g
from ele2038.model.mechanics import MechParams

def u_of_t(t: float) -> float:
    # constant voltage input (open-loop)
    return 5.0

def main():
    # --- Parameters (SI units) ---
    mech = MechParams(
        m=0.462,
        g=9.81,
        phi=np.deg2rad(41.0),
        k=1885.0,
        b=10.4,
        d=0.42,
        c=6.811e-3,
        delta=0.65,
        r=0.123,
    )

    elec = {
        "R": 2200.0,
        "L0": 0.125,
        "L1": 0.0241,
        "alpha": 1.2,
        "delta": 0.65,
    }

    sens = {
        "Km": 1.0,      # assumption (allowed by brief)
        "tau_m": 0.03,
    }

    params = {"mech": mech, "elec": elec, "sens": sens}

    # --- Initial state: [x, v, i, y] ---
    x0 = np.array([0.35, 0.0, 0.0, 0.35], dtype=float)

    t_span = (0.0, 5.0)
    t_eval = np.linspace(t_span[0], t_span[1], 1000)

    def rhs(t, x):
        return f(t, x, u_of_t(t), params)

    sol = solve_ivp(rhs, t_span, x0, t_eval=t_eval, rtol=1e-6, atol=1e-9)
    if not sol.success:
        raise RuntimeError(sol.message)

    # Compute output trajectory
    y = np.array([g(sol.y[:, k], u_of_t(sol.t[k]), params) for k in range(sol.y.shape[1])])

    # --- Plots ---
    plt.figure()
    plt.plot(sol.t, sol.y[0, :], label="x (position)")
    plt.plot(sol.t, sol.y[3, :], "--", label="y_m (sensor state)")
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.title("Open-loop nonlinear simulation (scaffold)")
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()