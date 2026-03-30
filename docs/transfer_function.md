# Transfer Function

## 1. Overview

The transfer function describes the relationship between the input and output of the linearised system in the Laplace domain.

For the linearised mechanical subsystem:

- Input: current deviation (ū)  
- Output: position deviation (x̄₁)  

---

## 2. Transfer Function from State-Space

The transfer function is obtained from the state-space model using:

G(s) = C(sI - A)^(-1)B + D  

---

## 3. State-Space Matrices

From the linearised model:

A =  
[ 0       1  
 -2691.2  -16.08 ]

B =  
[ 0  
  4.62 ]

C =  
[ 1  0 ]

D =  
[ 0 ]

---

## 4. Mechanical Transfer Function

Substituting the matrices into the transfer function expression gives:

G(s) = X̄₁(s) / Ī(s)

G(s) = 4.62 / (s^2 + 16.08s + 2691.2)

---

## 5. Sensor Dynamics

The sensor is modelled as a first-order system with time constant:

τm = 0.03 s  

Its transfer function is:

H(s) = 1 / (τm s + 1)

Substituting τm:

H(s) = 1 / (0.03s + 1)

---

## 6. Full System Transfer Function

The sensor is connected in series with the mechanical system, so the overall transfer function is:

G_total(s) = G(s) × H(s)

G_total(s) = 4.62 / [(s^2 + 16.08s + 2691.2)(0.03s + 1)]

---

## 7. Open-Loop Poles

The poles are the roots of the denominator.

### Mechanical poles

s^2 + 16.08s + 2691.2 = 0  

p₁ = -8.04 + 51.25j  
p₂ = -8.04 - 51.25j  

### Sensor pole

0.03s + 1 = 0  

p₃ = -33.33  

---

## 8. Stability Analysis

All poles have negative real parts:

- Mechanical poles have negative real components  
- Sensor pole is negative  

Therefore, the open-loop system is:

→ BIBO stable  

The complex poles indicate that the system is:

- underdamped  
- oscillatory in response  

---

## 9. Additional Interpretation

Comparing the denominator to the standard second-order form:

s^2 + 2ζωₙs + ωₙ^2  

We identify:

ωₙ = √2691.2 ≈ 51.9 rad/s  
ζ = 16.08 / (2 × 51.9) ≈ 0.155  

This confirms the system is lightly damped and will exhibit oscillations before settling.

---

## 10. Summary

The system has been converted from state-space form to a transfer function representation.

The full transfer function, including sensor dynamics, is:

G_total(s) = 4.62 / [(s^2 + 16.08s + 2691.2)(0.03s + 1)]

The open-loop system is stable and ready for controller design.
