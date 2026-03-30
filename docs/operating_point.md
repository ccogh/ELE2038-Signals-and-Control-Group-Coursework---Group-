# Operating Point

## 1. Equilibrium Conditions

The operating point is defined such that all state derivatives are zero:

$$
\dot{x}_1 = 0, \quad \dot{x}_2 = 0, \quad \dot{x}_3 = 0
$$

From the mechanical equation:

$$
0 =
\frac{5}{7m}
\left[
mg\sin\phi - k(x_0 - d) + \frac{c i_0^2}{(\delta - x_0)^2}
\right]
$$

Rearranging:

$$
mg\sin\phi - k(x_0 - d) + \frac{c i_0^2}{(\delta - x_0)^2} = 0
$$

---

## 2. Solving for Current

Rearranging for $i_0$:

$$
i_0^2 =
\frac{\left[k(x_0 - d) - mg\sin\phi\right](\delta - x_0)^2}{c}
$$

---

## 3. Feasibility Condition

For $i_0$ to be real:

$$
k(x_0 - d) - mg\sin\phi \ge 0
$$

This requires:

$$
x_0 > d
$$

---

## 4. Chosen Operating Point

To satisfy this condition and remain close to the desired setpoint, the operating point is chosen as:

$$
x_0 = 0.43 \, \text{m}, \quad v_0 = 0
$$

Substituting values gives:

$$
i_0 \approx 10.62 \, \text{A}
$$

---

## 5. Summary

The operating point used for linearisation is:

$$
(x_0, v_0, i_0)
$$
