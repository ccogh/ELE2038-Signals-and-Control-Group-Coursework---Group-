"""
Closed-loop simulation of the full nonlinear ball-on-incline system with PID control.

State vector:
    x1 = ball position [m]
    x2 = ball velocity [m/s]
    x3 = circuit current [A]
    x4 = sensor output [m]

Input:  V(t) = V0 + u_dev(t)   total applied voltage [V]
Output: y = x4                  sensor measurement
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
x_sp = 0.48                                    # setpoint [m]


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


def linear_step_response(x_sp, x0, t_eval):         # Absolute position response of linearised closed-loop system [m]
    # t_eval: time array [s]

    # closed-loop T(s) = C*GH / (1 + C*GH)
    t_num, t_den = closed_loop_num_den(Kp, Ki, Kd)
    T = control.tf(t_num, t_den)

    # step size is deviation from operating point
    step_size = x_sp - x0

    _, y_out = control.forced_response(T, T = t_eval, U = step_size * np.ones_like(t_eval))

    
    return x0 + y_out                               # reconstruct absolute position from deviation


def run_closed_loop(p, x_sp, x0, i0, t_end, dt):    # p: SystemParams instance

    if not is_valid_x0(x_sp):                       #Check setpoint is within valid range
        x0_min, x0_max = operating_point_limits()
        raise ValueError(f"x_sp = {x_sp} m is outside the valid range " f"[{x0_min:.3f}, {x0_max:.3f}) m")
    
    # equilibrium bias voltage calculation
    i_sp  = compute_i0(x_sp, p)    # equilibrium current at the setpoint
    V0    = p.R * i_sp                 # bias voltage correct for x_sp, not x0

    pid = PIDController(Kp, Ki, Kd, dt)
    state     = [x0, 0.0, i0, x0]
    t_current = 0.0

    print("Running closed-loop simulation...")
    print(f"  Setpoint:     x_sp = {x_sp} m")
    print(f"  Initial pos:  x0   = {x0} m")
    print(f"  Bias voltage: V0   = {V0:.1f} V")
    print(f"  PID gains:    Kp = {Kp}, Ki = {Ki}, Kd = {Kd}")
    print()

    n_steps = int(t_end / dt)

    t_history = [[0.0, x0, 0.0, i0, x0, V0]]                    # initialise storage lists

    for _ in range(n_steps):

        error = x_sp - state[3]                                  # error between setpoint and sensor output

        V_total  = V0 + pid.compute(error)                       # total voltage applied to electromagnet
        vin_func = lambda t, V = V_total: V

        
        sol = solve_ivp(lambda t, y: full_system_rhs(t, y, vin_func, p),
                        (t_current, t_current + dt), state)

        state = list(sol.y[:, -1])
        t_current += dt

        t_history.append([t_current, state[0], state[1], state[2], state[3], V_total])

    t_arr, x1_arr, x2_arr, x3_arr, x4_arr, V_arr = np.array(t_history).T

   
    x1_lin = linear_step_response(x_sp = x_sp, x0 = x0, t_eval = t_arr)   # linear model comparison for the same step

    
    steady_state = x1_arr[-1]                                       # print steady-state summary
    offset = abs(x_sp - steady_state)
    print("Simulation complete.")
    print(f"  Final position:     {steady_state:.4f} m")
    print(f"  Setpoint:           {x_sp:.4f} m")
    print(f"  Steady-state error: {offset:.2e} m")

    
    fig, axes = plt.subplots(5, 1, figsize = (10, 14), sharex = True)   # position: nonlinear vs linear model vs setpoint

    axes[0].plot(t_arr, x1_arr, label = "x1 - nonlinear")
    axes[0].plot(t_arr, x1_lin, "-", label = "x1 - linear model")
    axes[0].axhline(x_sp, color = "black", linewidth = 0.8, linestyle = ":", label = f"setpoint = {x_sp} m")
    axes[0].set_ylabel("x1 [m]")
    axes[0].set_title("Closed-loop simulation - nonlinear system with PID controller")
    axes[0].legend(loc = "upper right")
    axes[0].grid(True)

    # velocity
    axes[1].plot(t_arr, x2_arr, label = "x2 - velocity", color = "tab:orange")
    axes[1].axhline(0, color = "black", linewidth = 0.8, linestyle = "--")
    axes[1].set_ylabel("x2 [m/s]")
    axes[1].legend(loc = "upper right")
    axes[1].grid(True)

    # current
    axes[2].plot(t_arr, x3_arr, label = "x3 - current", color = "tab:green")
    axes[2].set_ylabel("x3 [A]")
    axes[2].legend(loc = "upper right")
    axes[2].grid(True)

    # sensor output vs true position
    axes[3].plot(t_arr, x4_arr, label = "x4 - sensor output", color = "tab:red")
    axes[3].plot(t_arr, x1_arr, "--", alpha = 0.4, label = "x1 (true)", color = "tab:blue")
    axes[3].axhline(x_sp, color = "black", linewidth = 0.8, linestyle = ":", label = f"setpoint = {x_sp} m")
    axes[3].set_ylabel("x4 [m]")
    axes[3].legend(loc = "upper right")
    axes[3].grid(True)

    # total applied voltage
    axes[4].plot(t_arr, V_arr, label = "V - total voltage", color = "tab:purple")
    axes[4].axhline(V0, color = "black", linewidth = 0.8, linestyle = "--", label = f"V0 = {V0:.0f} V")
    axes[4].set_ylabel("V [V]")
    axes[4].set_xlabel("Time [s]")
    axes[4].legend(loc = "upper right")
    axes[4].grid(True)

    plt.tight_layout()
    plt.savefig("closed_loop_simulation.svg")
    plt.show()
    print("Plot saved as closed_loop_simulation.svg")

if __name__ == "__main__":
    p = SystemParams()
    run_closed_loop(p, x_sp, x0, i0, t_end, dt)