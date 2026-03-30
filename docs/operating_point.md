# Operating Point

## 1. Equilibrium Conditions

The operating point is defined such that all state derivatives are zero:

ẋ₁ = 0, ẋ₂ = 0, ẋ₃ = 0  

From the mechanical equation:

0 = (5 / 7m) [ m g sin(φ) - k(x₀ - d) + (c i₀²) / (δ - x₀)² ]

Since (5 / 7m) ≠ 0, this simplifies to:

m g sin(φ) - k(x₀ - d) + (c i₀²) / (δ - x₀)² = 0  

---

## 2. Solving for Current

Rearranging for i₀:

i₀² = [ k(x₀ - d) - m g sin(φ) ] (δ - x₀)² / c  

---

## 3. Feasibility Condition

For i₀ to be real:

k(x₀ - d) - m g sin(φ) ≥ 0  

This requires:

x₀ > d  

---

## 4. Chosen Operating Point

To satisfy this condition and remain close to the desired setpoint, the operating point is chosen as:

x₀ = 0.43 m, v₀ = 0  

Substituting values gives:

i₀ ≈ 10.62 A  

---

## 5. Summary

The operating point used for linearisation is:

(x₀, v₀, i₀)
