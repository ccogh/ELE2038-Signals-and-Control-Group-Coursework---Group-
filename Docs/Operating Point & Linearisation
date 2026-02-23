# Mechanical operating point and linearisation

## 1. Coordinate convention and model scope
This document covers the **mechanical subsystem** only (ball + spring + damper + magnetic force), before coupling to the electrical circuit model.

### Coordinate convention
- `x`: position of the ball centre **along the incline**
- Positive `x` is **downhill**
- `v = x_dot`: velocity along the incline (positive downhill)

### Mechanical assumptions
- Rolling without slipping
- Ball is a solid sphere, so \(I = \frac{2}{5}mr^2\)
- Spring and damper act along the incline
- Magnetic attraction acts along the incline toward the electromagnet at \(x=\delta\)
- Air drag / rolling resistance neglected (separate from the given viscous damper)

---

## 2. Parameters (from coursework, SI units)
Using the coursework values (converted to SI where needed):

- \(m = 0.462\ \text{kg}\)
- \(g = 9.81\ \text{m/s}^2\)
- \(\phi = 41^\circ = 0.7156\ \text{rad}\)
- \(k = 1885\ \text{N/m}\)
- \(b = 10.4\ \text{N·s/m}\)
- \(d = 0.42\ \text{m}\)
- \(\delta = 0.65\ \text{m}\)
- \(r = 0.123\ \text{m}\)
- \(c = 6.811\ \text{m}^3\text{g}/(\text{A}^2\text{s}^2)\)

### Unit conversion for `c`
The coursework gives `c` with **grams** in the units, so for SI consistency:
- \(c = 6.811\times 10^{-3}\ \text{m}^3\text{kg}/(\text{A}^2\text{s}^2)\)

---

## 3. Nonlinear mechanical model (state-space)
From the force balance + rolling constraint, the mechanical acceleration is:

\[
\ddot x = \frac{5}{7m}\left[m g\sin\phi - k(x-d) - b\dot x + \frac{c i^2}{(\delta-x)^2}\right]
\]

Define the states:
- \(x_1 = x\)
- \(x_2 = v = \dot x\)

Then the nonlinear state model is:

\[
\dot x_1 = x_2
\]

\[
\dot x_2 = \frac{5}{7m}\left[m g\sin\phi - k(x_1-d) - b x_2 + \frac{c i^2}{(\delta-x_1)^2}\right]
\]

---

## 4. Operating point selection (equilibrium)
The coursework setpoint is around **0.4 m**. I tested the feasibility of a static equilibrium near this value.

### Equilibrium conditions
For an operating point \((x_0,v_0,i_0)\), equilibrium requires:
- \(v_0 = 0\)
- \(\ddot x_0 = 0\)

So the bracketed force balance must be zero:

\[
m g\sin\phi - k(x_0-d) + \frac{c i_0^2}{(\delta-x_0)^2}=0
\]

Rearranging for \(i_0\):

\[
i_0^2 = \frac{\left[k(x_0-d)-m g\sin\phi\right](\delta-x_0)^2}{c}
\]

### Important feasibility condition: the setpoint must be greater than `d`
For \(i_0\) to be real, we need \(i_0^2 \ge 0\). This requires:

\[
k(x_0-d)-m g\sin\phi \ge 0
\]

This implies the operating point must be chosen so that the spring provides an uphill restoring force. In practice, this means:

\[
\boxed{x_0 > d}
\]

With the coursework value \(d=0.42\ \text{m}\), a choice like \(x_0=0.40\ \text{m}\) gives **no real equilibrium current** (negative \(i_0^2\)), because gravity, spring (compressed), and magnet all act downhill.

### Chosen operating point
To obtain a valid equilibrium close to the coursework setpoint, I choose:

- \(\boxed{x_0 = 0.43\ \text{m}}\) (close to 0.4 m and satisfies \(x_0>d\))
- \(\boxed{v_0 = 0\ \text{m/s}}\)

Substituting the parameters gives:

- \(\boxed{i_0 \approx 10.62\ \text{A}}\)

This operating point is used for small-signal linearisation.

---

## 5. Linearisation
I linearised the nonlinear model about the operating point \((x_0,v_0,i_0)\) using the textbook (Chapter 3).

### Deviation variables
Define small deviations from the operating point:

\[
\bar x = x - x_0,\qquad \bar v = v - v_0,\qquad \bar i = i - i_0
\]

Since \(v_0=0\), this is simply \(\bar v=v\).

### Nonlinear magnetic term
Let:
\[
\phi(x,i)=\frac{c i^2}{(\delta-x)^2}
\]

The required partial derivatives are:

\[
\frac{\partial \phi}{\partial x} = \frac{2c i^2}{(\delta-x)^3}
\]

\[
\frac{\partial \phi}{\partial i} = \frac{2c i}{(\delta-x)^2}
\]

Evaluated at \((x_0,i_0)\):

\[
\left.\frac{\partial \phi}{\partial x}\right|_0 = \frac{2c i_0^2}{(\delta-x_0)^3},\qquad
\left.\frac{\partial \phi}{\partial i}\right|_0 = \frac{2c i_0}{(\delta-x_0)^2}
\]

### Linearised small-signal dynamics
The linearised mechanical model becomes:

\[
\dot{\bar x} = \bar v
\]

\[
\dot{\bar v}
=
\frac{5}{7m}\left(-k+\frac{2c i_0^2}{(\delta-x_0)^3}\right)\bar x
+
\frac{5}{7m}(-b)\bar v
+
\frac{5}{7m}\left(\frac{2c i_0}{(\delta-x_0)^2}\right)\bar i
\]

---

## 6. Linear state-space matrices (mechanics only)
Using the linearised state \(\bar{\mathbf{x}}=[\bar x\ \bar v]^T\) and input \(\bar u=\bar i\), the small-signal system is:

\[
\dot{\bar{\mathbf{x}}} = A\bar{\mathbf{x}} + B\bar u
\]
\[
\bar y = C\bar{\mathbf{x}} + D\bar u
\]

For output \(y=x\) (position), the matrices are:

\[
A =
\begin{bmatrix}
0 & 1\\
-2691.19868 & -16.0791589
\end{bmatrix}
\]

\[
B =
\begin{bmatrix}
0\\
4.62190956
\end{bmatrix}
\]

\[
C =
\begin{bmatrix}
1 & 0
\end{bmatrix}
,\qquad
D =
\begin{bmatrix}
0
\end{bmatrix}
\]

These values were computed at:
- \(x_0 = 0.43\ \text{m}\)
- \(v_0 = 0\ \text{m/s}\)
- \(i_0 \approx 10.62\ \text{A}\)

---

## 7. Linearisation validation (nonlinear vs linear model)
A small-step test in current (\(\Delta i\)) was applied at the operating point and the nonlinear and linearised responses were compared.

### Result
The nonlinear and linearised position responses overlap almost exactly for a small perturbation, confirming that the linear model is a valid **local approximation** around the operating point.

### Figure
Include the comparison plot here (example filename):
- `fig_linearisation_check_position.png`

Suggested caption:
> Comparison of nonlinear and linearised mechanical position response for a small current step about \((x_0,v_0,i_0)\). The close match validates the small-signal linearisation.

---

## 8. Handoff to the next stage (Laplace / transfer function)
This mechanical linearisation is now ready to be used for:
- transfer function derivation (Laplace transform),
- local stability analysis,
- controller design.

Note: this is the **mechanics-only** model with input `current i`. The full coursework system will later use **input voltage \(V\)** once the electrical subsystem is coupled in (so \(i\) becomes a state rather than the direct input).
