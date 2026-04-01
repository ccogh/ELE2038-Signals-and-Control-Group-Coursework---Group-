# Electrical and Sensor Modelling

The aim of this section is to derive the electrical circuit dynamics of the electromagnet and the measurement equation for the sensor.

---

## 1. Variables

- x₁(t): position of the ball (m)  
- x₃(t): current in the circuit (A)  
- u(t): input voltage (V)  
- R: resistance (Ω)  
- L(x₁): inductance (H)  
- yₘ(t): measured position (sensor output)  
- δ: fixed position of the electromagnet (m), used to define the distance between the ball and magnet as (δ - x₁)

---

## 2. Distance Relation

The distance between the ball and the electromagnet is:

y(t) = δ - x₁(t)

The electromagnetic force depends on the distance y, not directly on the position x₁.

---

## 3. Inductance Model

The inductance of the electromagnet varies with position and is given by:

L(x₁) = L₀ + L₁ e^(-α(δ - x₁))

This shows that the inductance changes as the ball moves, making the system nonlinear.

---

## 4. Electrical Model

Applying Kirchhoff’s Voltage Law (KVL):

u(t) = R x₃(t) + d/dt (L(x₁) x₃(t))

Using the product rule:

d/dt (L x₃) = L(x₁) ẋ₃ + x₃(t) L̇

So:

u(t) = R x₃(t) + L(x₁) ẋ₃ + x₃(t) L̇

---

## 5. Modelling Assumption

**Assumption A1:** The term x₃(t) L̇ is neglected.

This term arises due to the position dependence of the inductance, where:

L̇ = (dL/dx₁) ẋ₁

and therefore introduces coupling between the electrical and mechanical dynamics through the velocity x₂.

Near the operating point, the velocity is small (x₂ ≈ 0), so L̇ is small and the contribution of the term x₃(t) L̇ can be neglected.

This simplifies the electrical model and allows the system to be analysed and linearised more easily. This is an approximation, not an exact step.

---

## 6. Electrical State Equation

With this assumption:

u(t) ≈ R x₃(t) + L(x₁) ẋ₃

Rearranging:

ẋ₃ = (u(t) - R x₃(t)) / L(x₁)

This is the electrical state equation used in the nonlinear model.

---

## 7. Sensor Model

The sensor is modelled as a first-order system with time constant τₘ:

τₘ ẏₘ + yₘ = x₁(t)

Rearranging:

ẏₘ = (x₁(t) - yₘ(t)) / τₘ

---

## 8. Output Definition

The measured output of the system is:

y = yₘ
