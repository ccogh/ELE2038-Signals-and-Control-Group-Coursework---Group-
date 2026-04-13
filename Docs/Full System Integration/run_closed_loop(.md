# Closed-Loop Simulation

## Purpose

This script runs a closed-loop simulation of the full nonlinear ball-on-incline system with a PID controller. It tests whether the controller designed from the linearised model works on the real nonlinear system, and identifies the valid setpoint range around the operating point x0 = 0.50 m.


## Dependencies

| File | Provides |
|------|----------|
| `full_system.py` | `SystemParams`, `full_system_rhs` - nonlinear ODE and system parameters |
| `pid.py` | `Kp`, `Ki`, `Kd`, `closed_loop_num_den` - gains and closed-loop transfer function |
| `linearise_mechanics.py` | `Params`, `compute_i0` - equilibrium current at operating point and setpoint |
| `mechanics_2.py` | `is_valid_x0`, `operating_point_limits` - setpoint validation before simulation |


## How to Run

```
python run_closed_loop.py
```

Set the desired setpoint by changing `x_sp` at the top of the file. The script validates the chosen setpoint against the valid operating range using `is_valid_x0` from `mechanics_2.py`, produces a five-panel plot, and prints the final position and steady-state error to the console. The plot is saved as `closed_loop_simulation.png`.


## Bias Voltage Correction

The equilibrium bias voltage V0 is computed at the setpoint rather than the operating point:

```python
i_sp = compute_i0(x_sp, p)
V0   = p.R * i_sp
```

Without this correction the integral term winds up indefinitely because the bias voltage is calibrated for x0 = 0.50 m rather than the target position, causing the current and voltage to drift without settling.


## Simulation Results

The controller was tested at several setpoints. Key results:

| Setpoint | Result |
|----------|--------|
| 0.50 m | No step - no correction necessary |
| 0.52 m | Settles cleanly at setpoint |
| 0.48 m | Settles cleanly at setpoint |
| 0.45 m | Settles cleanly at setpoint |
| 0.40 m | Does not reach setpoint - setpoint outside appropriate range |
| 0.55 m | Unstable - overshoot drives ball into electromagnet |

The controller works well for small deviations close to x0 = 0.50 m, consistent with the linearisation being valid only in a neighbourhood of the operating point.


## Valid Setpoint Range

The lower bound is set by the spring natural length d = 0.42 m. Below this value no real equilibrium current exists and `compute_i0` raises a `ValueError`. The upper bound is between 0.52 m and 0.55 m - at 0.55 m the 81% overshoot carries the ball close enough to the electromagnet that the magnetic force overwhelms the controller and the system diverges.

The practical operating range is therefore approximately: 0.43 m ≤ x_sp ≤ 0.52 m


## Limitations

- The controller was designed from a linearised model at x0 = 0.50 m and loses accuracy for larger setpoint deviations
- The equilibrium voltage V0 ≈ 48,620 V is unrealistically large for a physical implementation
- The closed-loop response shows approximately 81% overshoot, consistent with the phase margin of 41.4° reported in `stability_margins.md`
- The upper setpoint limit is determined by the overshoot carrying the ball too close to the electromagnet during the transient, not by the equilibrium physics
- The linear and nonlinear step responses diverge for larger steps, confirming the linearisation is only locally valid