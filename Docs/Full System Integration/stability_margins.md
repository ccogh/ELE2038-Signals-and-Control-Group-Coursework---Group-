# Stability Margins

## 1. Overview

This document reports the gain and phase margins of the closed-loop system, computed from the open-loop transfer function L(s) = C(s)·GH(s) using `bode.py`.


## 2. Transfer Functions

| Symbol | Description |
|--------|-------------|
| GH(s) | Combination of G(s) [Linearised plant (voltage → position)] and<br>H(s) [Sensor dynamics, first-order, τₘ = 0.03 s]|
| C(s) | PID controller, Kp = 32000, Ki = 20000, Kd = 1500 |
| L(s) | Open-loop: C(s)·GH(s) |


## 3. Stability Margins

| Quantity | Value |
|----------|-------|
| Phase margin (PM) | 41.4° |
| Gain margin (GM) | 0.465 (-6.64 dB) - see note below |
| Gain crossover frequency (ωgc) | 11.20 rad/s |
| Phase crossover frequency (ωpc) | 2.17 rad/s |


## 4. Robustness Assessment

For the sake of the stability assessment, a reasonable target of 45° has been set.

The measured phase margin of 41.4° is just below this target. Ths suggests that the proposed system is stable, however its robustness is questionable, meaning:

- Small changes in plant parameters (spring stiffness, damping, magnetic force constant) could degrade the response
- Additional phase lag from unmodelled dynamics (for example, a more accurate sensor model or actuator delay) could further reduce the margin
- The closed-loop step response showing approximately 81% overshoot is consistent with a phase margin in this range


## 5. Note on Gain Margin and Bode Stability Criterion

The gain margin of −6.64 dB appears to indicate instability, but this reading cannot be trusted for this system. The Bode stability criterion assumes the open-loop system is stable, which is not the case here due to the right-half-plane (RHP) pole in the plant. Additionally, the phase curve crosses −180° twice rather than once, which means the single gain margin value reported by `control.margin()`is ambiguous. For these reasons the Routh criterion, which confirms all closed-loop poles have negative real parts, has been used as the definitive stability proof instead.


## 6. Summary

The PID controller with gains Kp = 32000, Ki = 20000, Kd = 1500 effectively stabilises the closed-loop system, and the phase margin of 41.4° falls within an acceptable range from the 45° target. The gain margin of -6.64 dB is not a reliable indicator of instability here due to the RHP pole in the plant, as such stability is proven using the Routh criterion. The large overshoot observed in simulation is consistent with the phase margin in this range and represents the main performance limitation of the selected controller.