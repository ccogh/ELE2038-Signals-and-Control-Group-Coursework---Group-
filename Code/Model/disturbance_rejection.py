"""
Copy of run_closed_loop.py with changes added to implement a disturbance
and display how the controller handles this.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import control

                # PID gains   
from pid import Kp, Ki, Kd, closed_loop_num_den
from full_system import SystemParams, full_system_rhs   
from linearise_mechanics import Params, compute_i0
from mechanics_2 import is_valid_x0, operating_point_limits

# equilibrium operating point
x0 = 0.50                                           # ball position [m]
i0 = compute_i0(x0, Params())                       # circuit current [A]
dt = 0.001                                          # controller timestep [s]
t_end = 5.0                                         # simulation duration [s]
x_sp = 0.48                                         # setpoint [m]


# disturbance parameters
t_dist   = 3.0      # time at which disturbance is applied [s]
dist_dur = 0.2      # duration of disturbance [s]
dist_mag = 1500.0   # disturbance magnitude [V]


class PIDController:                                # discrete-time PID controller
    def __init__(self, Kp, Ki, Kd, dt):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt
        self.integral   = 0.0
        self.prev_error = None

    def reset(self):                                # resets integral and previous error
        self.integral   = 0.0
        self.prev_error = None

    def compute(self, error):                       # error: e(t) = x_sp - x4
        self.integral += error * self.dt            # integral term using rectangle rule

        if self.prev_error is None:
            derivative = 0.0
        else:
            derivative = (error - self.prev_error) / self.dt    # derivative term using backward Euler

        self.prev_error = error

        return self.Kp * error + self.Ki * self.integral + self.Kd * derivative

# SystepParams, setpoint [m], initial position/operating point, equilibrium current (A),
# disturbance time [s], disturbance duration[s], disturbance magnitude [V]
def run_disturbance_rejection(p, x_sp, x0, i0, t_end, dt, t_dist, dist_dur, dist_mag):

    if not is_valid_x0(x_sp):
        x0_min, x0_max = operating_point_limits()
        raise ValueError(f"x_sp = {x_sp} m is outside valid range [{x0_min:.3f}, {x0_max:.3f}) m")

    # bias voltage computed at setpoint to avoid steady-state error
    i_sp = compute_i0(x_sp, p)
    V0   = p.R * i_sp

    pid     = PIDController(Kp, Ki, Kd, dt)
    state   = [x0, 0.0, i0, x0]
    t_current = 0.0
    n_steps   = int(t_end / dt)

    print("Running disturbance rejection simulation...")
    print(f"  Setpoint:          x_sp     = {x_sp} m")
    print(f"  Bias voltage:      V0       = {V0:.1f} V")
    print(f"  Disturbance time:  t_dist   = {t_dist} s")
    print(f"  Disturbance mag:   dist_mag = {dist_mag:.0f} V")
    print()

    t_history = [[0.0, x0, 0.0, i0, x0, V0, 0.0]]   # last column stores disturbance

    for _ in range(n_steps):
        error = x_sp - state[3]

        # disturbance active between t_dist and t_dist + dist_dur
        d = dist_mag if t_dist <= t_current < t_dist + dist_dur else 0.0

        V_total  = V0 + pid.compute(error) + d        # total voltage including disturbance
        vin_func = lambda t, V = V_total: V

        sol   = solve_ivp(lambda t, y: full_system_rhs(t, y, vin_func, p),
                          (t_current, t_current + dt), state)
        state = list(sol.y[:, -1])
        t_current += dt

        t_history.append([t_current, state[0], state[1], state[2], state[3], V_total, d])

    t_arr, x1_arr, x2_arr, x3_arr, x4_arr, V_arr, d_arr = np.array(t_history).T

    steady_state = x1_arr[-1]                                       # print steady-state summary
    offset = abs(x_sp - steady_state)
    print("Simulation complete.")
    print(f"  Final position:     {steady_state:.4f} m")
    print(f"  Setpoint:           {x_sp:.4f} m")
    print(f"  Steady-state error: {offset:.2e} m")

    # three panel plot: position, voltage, disturbance signal
    fig, axes = plt.subplots(3, 1, figsize = (10, 9), sharex = True)

    # position
    axes[0].plot(t_arr, x1_arr, label = "x1 - ball position", color = "tab:blue")
    axes[0].axhline(x_sp, color = "black", linewidth = 0.8, linestyle = ":",
                    label = f"setpoint = {x_sp} m")
    axes[0].axvspan(t_dist, t_dist + dist_dur, alpha = 0.15, color = "tab:red",
                    label = "disturbance active")
    axes[0].set_ylabel("x1 [m]")
    axes[0].set_title("Disturbance rejection -- closed-loop nonlinear system")
    axes[0].legend(loc = "upper right")
    axes[0].grid(True)

    # voltage
    axes[1].plot(t_arr, V_arr, label = "V - total voltage", color = "tab:purple")
    axes[1].axhline(V0, color = "black", linewidth = 0.8, linestyle = "--",
                    label = f"V0 = {V0:.0f} V")
    axes[1].axvspan(t_dist, t_dist + dist_dur, alpha = 0.15, color = "tab:red")
    axes[1].set_ylabel("V [V]")
    axes[1].legend(loc = "upper right")
    axes[1].grid(True)

    # disturbance signal
    axes[2].plot(t_arr, d_arr, label = "d(t) - disturbance", color = "tab:red")
    axes[2].set_ylabel("d [V]")
    axes[2].set_xlabel("Time [s]")
    axes[2].legend(loc = "upper right")
    axes[2].grid(True)

    plt.tight_layout()
    plt.savefig("disturbance_rejection.svg")
    plt.show()
    print("Plot saved as disturbance_rejection.svg")


if __name__ == "__main__":
    p = SystemParams()
    run_disturbance_rejection(p, x_sp, x0, i0, t_end, dt, t_dist, dist_dur, dist_mag)