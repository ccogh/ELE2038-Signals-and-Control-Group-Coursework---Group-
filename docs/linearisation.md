# Linearisation of the Nonlinear Model

## 1. Overview

The nonlinear system is linearised about the operating point using a small-signal approximation.

This allows the system to be approximated as a linear system for small deviations about the equilibrium.

The linear system is expressed in deviation form as:

ẋ̄ = A x̄ + B ū  
ȳ = C x̄ + D ū  

---

## 2. Nonlinear System

The nonlinear state equations are:

ẋ₁ = x₂  

ẋ₂ = (5 / 7m) [ m g sin(φ) - k(x₁ - d) - b x₂ + c x₃² / (δ - x₁)² ]  

ẋ₃ = (u - R x₃) / L(x₁)  

where:

L(x₁) = L₀ + L₁ e^(-α(δ - x₁))

---

## 3. Linearisation Method

The system is linearised about the operating point:

(x_{1,0}, x_{2,0}, x_{3,0}, u₀)

using a first-order Taylor expansion.

This gives:

ẋ̄ = A x̄ + B ū  

where:

A = ∂f/∂x evaluated at the operating point  
B = ∂f/∂u evaluated at the operating point  

---

## 4. Linearised Equations

The linearised system takes the form:

ẋ̄₁ = x̄₂  

ẋ̄₂ = a₁ x̄₁ + a₂ x̄₂ + a₃ x̄₃  

ẋ̄₃ = b₁ x̄₁ + b₂ x̄₃ + b₃ ū  

---

## 5. Coefficients

The coefficients are obtained from partial derivatives of the nonlinear system:

a₁ = ∂(ẋ₂)/∂x₁  
a₂ = ∂(ẋ₂)/∂x₂  
a₃ = ∂(ẋ₂)/∂x₃  

b₁ = ∂(ẋ₃)/∂x₁  
b₂ = ∂(ẋ₃)/∂x₃  
b₃ = ∂(ẋ₃)/∂u  

evaluated at (x_{1,0}, x_{2,0}, x_{3,0}, u₀)

---

## 6. State-Space Representation

The linearised system can be written as:

A =  
[ 0    1    0  
  a₁   a₂   a₃  
  b₁   0    b₂ ]

B =  
[ 0  
  0  
  b₃ ]

C =  
[ 1  0  0 ]

D =  
[ 0 ]

---

## 7. Numerical Values

Using the operating point x_{1,0} = 0.50 m, x_{2,0} = 0 and x_{3,0} ≈ 22.1 A, the coefficients are approximately:

a₁ ≈ 133.0  
a₂ ≈ -16.08  
a₃ ≈ 20.68  

b₁ = 0  
b₂ ≈ -15158.82  
b₃ ≈ 6.89  

So the numerical state-space model is:

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

## 8. Interpretation

- The system is third-order, with states representing position, velocity, and current  
- The input is the voltage deviation ū  
- The output is the position deviation x̄₁  
- The second row of A represents the mechanical dynamics  
- The third row of A represents the electrical dynamics  

---

## 9. Summary

The nonlinear system has been linearised about the operating point, resulting in a third-order linear state-space model.

This model will be used to derive the transfer function and design the controller.
