# Full System Model

## Purpose

This script combines the mechanical, electrical, and sensor subsystems of the ball-on-incline system into a single four-state nonlinear ODE and runs an open-loop simulation.

---

## State Vector

| State | Variable | Description | Units |
|-------|----------|-------------|-------|
| x1 | x | Ball position along the incline (positive downhill) | m |
| x2 | v | Ball velocity along the incline | m/s |
| x3 | i | Current in the electromagnet circuit | A |
| x4 | xₘ | Sensor output (measured position) | m |

**Input:** Applied voltage V [V]

**Output:** y = x4 (sensor measurement)

---

## Dependencies

| File | Provides |
|------|----------|
| `mechanics.py` | `mech_rhs()` - mechanical acceleration from Newton's second law and rolling constraint |
| `electrical.py` | `di_dt()` - rate of change of current from Kirchhoff's voltage law |
| `sensor.py` | `sensor_deriv()` - first-order sensor ODE |

---

## Assumptions

1.  **Rolling without slipping** - the ball rolls on the incline with no sliding.  This gives an effective mass of (7/5)m, derived from the moment of inertia of a solid sphere I = (2/5)mr².

2.  **Solid sphere** - the ball is treated as isotropic with uniform mass distribution, as stated in the coursework brief.

3.  **Assumption A1 - iL term neglected** - the full electrical ODE derived from KVL is:

        V = Ri + L(x)*(di/dt) + i*(dL/dt)

    The term i*(dL/dt) couples the electrical and mechanical dynamics through the ball velocity.Near the operating point the velocity x2 ≈ 0, making dL/dt ≈ 0, so this term is negligible.  Dropping it gives the simplified form used in `electrical.py`:

        di/dt = (V - R*i) / L(x1)

    This is an approximation, valid in the range of the equilibrium point.  See `electrical_sensor_derivation.md` for full justification.

4.  **Sensor gain Km = 1** - A unity gain is assumed, meaning the sensor output equals the true position at steady state.

5.  **Air resistance neglected** - only the viscous damper modelled in the spring-damper assembly is included.  Additional drag forces are not modelled.

---

## How to Run

Ensure `mechanics.py`, `electrical.py`, and `sensor.py` are in the same directory, then run:

```
python full_system.py
```

This will print the operating point parameters to the console and display five plots showing x1, x2, x3, x4, and Vᵢₙ over 0.5 seconds.

---

## Open-Loop Behaviour

This open-loop system is unstable.  The linearised transfer function analysis (see `transfer_function.md`) identifies a right-half-plane pole at approximately +6 rad/s, which causes any small deviation from equilibrium to grow exponentially over time.

This behaviour is expected, and demonstrates why feedback control is necessary.   Without a controller actively adjusting the voltage in response to position error, the system cant maintain the ball at the setpoint.

---

## Operating Point

The simulation is initialised at the equilibrium operating point:

| Quantity | Value |
|----------|-------|
| Ball position x1,0 | 0.5 m |
| Ball velocity x2,0 | 0.00 m/s |
| Circuit current x3,0 | 22.1 A |
| Sensor output x4,0 | 0.5 m |
| Input voltage V0 | 48,620 V |

The equilibrium voltage V0 = R × i0 = 2200 × 22.1 ≈ 48,620 V is high due to the large resistance R = 2.2 kΩ.
