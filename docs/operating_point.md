# Operating Point

## 1. Equilibrium Conditions

The operating point is defined such that all state derivatives are zero:

ẋ₁ = 0, ẋ₂ = 0, ẋ₃ = 0  

---

## 2. Mechanical Equilibrium

From the mechanical equation:

0 = (5 / 7m) [ m g sin(φ) - k(x₁,₀ - d) + (c x₃,₀²) / (δ - x₁,₀)² ]

Since (5 / 7m) ≠ 0, this simplifies to:

m g sin(φ) - k(x₁,₀ - d) + (c x₃,₀²) / (δ - x₁,₀)² = 0  

---

## 3. Solving for Current

Rearranging for the equilibrium current x₃,₀:

x₃,₀² = [ k(x₁,₀ - d) - m g sin(φ) ] (δ - x₁,₀)² / c  

---

## 4. Electrical Equilibrium

From the electrical state equation:

ẋ₃ = (u - R x₃) / L(x₁)

At equilibrium:

0 = (u₀ - R x₃,₀) / L(x₁,₀)

Since L(x₁,₀) ≠ 0:

u₀ = R x₃,₀  

---

## 5. Chosen Operating Point

The system is linearised about a nominal operating position:

x₁,₀ = 0.50 m  

with:

x₂,₀ = 0  

The corresponding equilibrium current x₃,₀ is obtained from the mechanical equilibrium equation, and the equilibrium voltage is:

u₀ = R x₃,₀  

For this operating point, the current is approximately:

x₃,₀ ≈ 22.1 A  

---

## 6. Operating Region

The system is designed to operate near the setpoint:

x₁ ≈ 0.50 m  

Performance will be assessed for nearby setpoints (e.g. 0.46 m to 0.54 m) to evaluate robustness of the controller.

---

## 7. Feasibility Condition

For x₃,₀ to be real:

x₁,₀ ≥ d + (m g sin(φ)) / k  

This ensures that a real equilibrium current exists at the chosen operating point.  

---

## 8. Final Operating Point

The operating point used for linearisation is:

(x₁,₀, x₂,₀, x₃,₀, u₀)
