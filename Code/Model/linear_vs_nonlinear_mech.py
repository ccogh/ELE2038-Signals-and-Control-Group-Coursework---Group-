from __future__ import annotations
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

#import from existing files
from mechanics import MechParams, mech_rhs
from linearise_mechanics import Params, compute_i0, linearise_mechanics


def build_params() -> tuple[MechParams, Params]:
    #nonlinear mechanics params
    p_nl = MechParams(
        m=0.462,
        g=9.81,
        phi=math.radians(41.0),
        k=1885.0,
        b=10.4,
        d=0.42,
        c=6.811e-3, 
        delta=0.65,
        r=0.123,
        eps=1e-9,
    )

    #linearisation params
    p_lin = Params(
        m=0.462,
        g=9.81,
        phi=math.radians(41.0),
        k=1885.0,
        b=10.4,
        d=0.42,
        delta=0.65,
        c=6.811e-3,
        eps=1e-9,
    )

    return p_nl, p_lin


def current_step(t: float, i0: float, di: float, t_step: float) -> float:
    return i0 + (di if t >= t_step else 0.0)


def delta_current_step(t: float, di: float, t_step: float) -> float:
    return di if t >= t_step else 0.0


def nonlinear_rhs_factory(p_nl: MechParams, i0: float, di: float, t_step: float):
    def rhs(t: float, state: np.ndarray) -> np.ndarray:
        i_t = current_step(t, i0=i0, di=di, t_step=t_step)
        x_dot, v_dot = mech_rhs(t, (float(state[0]), float(state[1])), i=i_t, p=p_nl)
        return np.array([x_dot, v_dot], dtype=float)
    return rhs


def linear_rhs_factory(A: np.ndarray, B: np.ndarray, di: float, t_step: float):
    def rhs(t: float, z: np.ndarray) -> np.ndarray:
        du = delta_current_step(t, di=di, t_step=t_step)
        return (A @ z.reshape(-1, 1) + B * du).ravel()
    return rhs


def main() -> None:
    x0 = 0.43   # operating point
    v0 = 0.0    #m/s
    t0 = 0.0
    tf = 0.5    
    t_eval = np.linspace(t0, tf, 1200)

    di = 0.5    #step in current
    t_step = 0.05   #s

    p_nl, p_lin = build_params()

    i0 = compute_i0(x0, p_lin)
    A, B, C, D = linearise_mechanics(x0=x0, i0=i0, p=p_lin)

    print(f"x0 = {x0:.3f} m, v0 = {v0:.3f} m/s, i0 = {i0:.6f} A")
    print("A =\n", A)
    print("B =\n", B)
    print("C =\n", C)
    print("D =\n", D)

    #Nonlinear simulation
    nl_rhs = nonlinear_rhs_factory(p_nl=p_nl, i0=i0, di=di, t_step=t_step)
    x_init_nl = np.array([x0, v0], dtype=float)

    sol_nl = solve_ivp(
        fun=nl_rhs,
        t_span=(t0, tf),
        y0=x_init_nl,
        t_eval=t_eval,
        rtol=1e-8,
        atol=1e-10,
    )

    if not sol_nl.success:
        raise RuntimeError(f"Nonlinear simulation failed: {sol_nl.message}")

    x_nl = sol_nl.y[0, :]
    v_nl = sol_nl.y[1, :]
    dx_nl = x_nl - x0
    dv_nl = v_nl - v0

    #Linear simulation
    lin_rhs = linear_rhs_factory(A=A, B=B, di=di, t_step=t_step)
    z_init = np.array([0.0, 0.0], dtype=float)

    sol_lin = solve_ivp(
        fun=lin_rhs,
        t_span=(t0, tf),
        y0=z_init,
        t_eval=t_eval,
        rtol=1e-9,
        atol=1e-11,
    )

    if not sol_lin.success:
        raise RuntimeError(f"Linear simulation failed: {sol_lin.message}")

    dx_lin = sol_lin.y[0, :]
    dv_lin = sol_lin.y[1, :]

    #Plots
    fig, axes = plt.subplots(3, 1, figsize=(9, 10), sharex=True)

    # 1) Position deviation
    axes[0].plot(sol_nl.t, dx_nl, label="Nonlinear Δx")
    axes[0].plot(sol_lin.t, dx_lin, "--", label="Linear Δx")
    axes[0].set_ylabel("Δx [m]")
    axes[0].set_title("Linearisation check: position deviation")
    axes[0].grid(True)
    axes[0].legend()

    # 2) Velocity deviation
    axes[1].plot(sol_nl.t, dv_nl, label="Nonlinear Δv")
    axes[1].plot(sol_lin.t, dv_lin, "--", label="Linear Δv")
    axes[1].set_ylabel("Δv [m/s]")
    axes[1].set_title("Linearisation check: velocity deviation")
    axes[1].grid(True)
    axes[1].legend()

    # 3) Absolute position
    axes[2].plot(sol_nl.t, x_nl, label="Nonlinear x")
    axes[2].plot(sol_lin.t, x0 + dx_lin, "--", label="Linear x (reconstructed)")
    axes[2].set_xlabel("Time [s]")
    axes[2].set_ylabel("x [m]")
    axes[2].set_title("Absolute position around operating point")
    axes[2].grid(True)
    axes[2].legend()

    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()
