# Linearisation of the Nonlinear Model

## 1. Overview

The nonlinear system is linearised about the operating point using a small-signal approximation.

This allows the system to be approximated as a linear system for small deviations about the equilibrium.

The linear system will be expressed in the form:

dx̄/dt = A x̄ + B ū  
ȳ = C x̄ + D ū  

---

## 2. Nonlinear Term

The nonlinear magnetic force term is:

φ(x, i) = c i² / (δ - x)²

This term introduces nonlinearity into the system and must be linearised.

---

## 3. Partial Derivatives

The partial derivatives of φ with respect to x and i are:

∂φ/∂x = 2c i² / (δ - x)³  

∂φ/∂i = 2c i / (δ - x)²  

These are evaluated at the operating point (x₀, i₀).

---

## 4. Linearised Mechanical Model

Using deviation variables and substituting the derivatives into the mechanical equation:

dx̄₁/dt = x̄₂  

dx̄₂/dt = a₁ x̄₁ + a₂ x̄₂ + b x̄₃  

where:

a₁ = (5 / 7m)[ -k + (2c i₀² / (δ - x₀)³) ]  

a₂ = (5 / 7m)(-b)  

b = (5 / 7m)[ (2c i₀ / (δ - x₀)²) ]  

---

## 5. State-Space Representation

The linearised system in deviation form can be written as:

A =  
[ 0   1  
  a₁  a₂ ]

B =  
[ 0  
  b ]

C =  
[ 1  0 ]

D =  
[ 0 ]

---

## 6. Numerical Values

Substituting the operating point values gives:

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

## 7. Summary

The nonlinear system has been linearised about the operating point, resulting in a second-order linear system.

This linear model will be used to derive the transfer function and design the controller.
