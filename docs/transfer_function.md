# Transfer Function

## 1. Overview

The transfer function describes the relationship between the input and output of the linearised system in the Laplace domain.

For the linearised plant:

- Input: voltage deviation (ū)  
- Output: position deviation (x̄₁)  

The plant is first derived from the 3-state linearised model. The sensor is then included separately as a first-order block.

---

## 2. Transfer Function from State-Space

The plant transfer function is obtained from the state-space model using:

G(s) = C(sI - A)^(-1)B + D  

For the linearised system:

ẋ̄ = A x̄ + B ū  
ȳ = C x̄ + D ū  

with output ȳ = x̄₁.

---

## 3. State-Space Matrices

From the linearised 3-state model:

A =  
[ 0        1         0  
  133.0   -16.08    20.68  
  0        0     -15158.82 ]

B =  
[ 0  
  0  
  6.89 ]

C =  
[ 1  0  0 ]

D =  
[ 0 ]

---

## 4. Plant Transfer Function

Substituting the matrices into the state-space transfer function formula gives the plant transfer function:

G(s) = X̄₁(s) / Ū(s)

Using the linearised model, this gives approximately:

G(s) = 142.5 / (s³ + 15170 s² + 243600 s - 2016000)

This is the transfer function of the linearised plant from voltage deviation to position deviation.

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

The sensor is connected in series with the plant, so the overall transfer function is:

G_total(s) = G(s) × H(s)

So the full measured-output transfer function is:

G_total(s) = 142.5 / [(s³ + 15170 s² + 243600 s - 2016000)(0.03s + 1)]

---

## 7. Open-Loop Poles

The poles of the plant are the roots of:

s³ + 15170 s² + 243600 s - 2016000 = 0

Using Python, the plant poles are approximately:

p₁ ≈ -15158.82  
p₂ ≈ -22.10  
p₃ ≈ 6.02  

The sensor contributes an additional pole:

p₄ = -33.33  

---

## 8. Stability Analysis

The open-loop plant is not BIBO stable, because one pole lies in the right half-plane:

- p₃ ≈ 6.02  

The other poles are in the left half-plane:

- p₁ ≈ -15158.82  
- p₂ ≈ -22.10  
- sensor pole p₄ = -33.33  

Therefore, the full open-loop system is:

→ unstable  

This means feedback control is required to stabilise the system around the operating point.

---

## 9. Interpretation

The linearised plant is third-order because it contains three states:

- position  
- velocity  
- current  

The electrical pole is very fast compared with the mechanical poles, which reflects the much faster current dynamics.

The presence of a right-half-plane pole indicates that the open-loop system is unstable near the chosen operating point. This is important for controller design.

---

## 10. Summary

The corrected transfer function is derived from the 3-state voltage-input linearised plant.

The plant transfer function is:

G(s) = 142.5 / (s³ + 15170 s² + 243600 s - 2016000)

Including the sensor gives:

G_total(s) = 142.5 / [(s³ + 15170 s² + 243600 s - 2016000)(0.03s + 1)]

The full open-loop system is unstable because of one right-half-plane pole, so controller design is necessary.
