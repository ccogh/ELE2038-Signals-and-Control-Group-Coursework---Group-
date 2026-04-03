# PID Controller Section Notes

## Controller structure

The controller is designed in **deviation variables** around the feasible operating point $x_0 = 0.50\,\text{m}$. The time-domain PID law is

$$
u_{\text{dev}}(t)=K_p e(t)+K_i\int_0^t e(\tau)\,d\tau + K_d \dot e(t)
$$

where $e(t)=r(t)-y(t)$. In the Laplace domain,

$$
C(s)=K_p+\frac{K_i}{s}+K_d s
=\frac{K_d s^2+K_p s+K_i}{s}
$$

If the plant transfer function is $G(s)$ and the sensor transfer function is $H(s)$, then

$$
L(s)=C(s)G(s)H(s),
\qquad
T(s)=\frac{C(s)G(s)}{1+C(s)G(s)H(s)},
\qquad
S(s)=\frac{1}{1+C(s)G(s)H(s)}
$$

The integral term makes the controller **type-1**, so for a stable closed loop it is expected to give **zero steady-state error to a constant reference** and improved rejection of **constant disturbances**.

## Bias voltage and deviation input

Because the linear model is built around a non-zero equilibrium, the PID output is not the full physical input. The total voltage applied to the electromagnet is

$$
V(t)=V_0+u_{\text{dev}}(t)
$$

At equilibrium, the inductor voltage is zero, so

$$
V_0=Ri_0
$$

For the chosen operating point $x_0=0.50\,\text{m}$, the equilibrium current is approximately

$$
i_0 \approx 22.1\,\text{A}
$$

so with $R=2.2\,\text{k}\Omega$,

$$
V_0 \approx 2200\times 22.1 \approx 4.86\times 10^4\,\text{V}
$$

This large bias voltage is a practical limitation of the system and should be discussed clearly in the report.

## PID gains tested

Three candidate gain sets were tested using the **Routh criterion**, **closed-loop poles**, and **step-response simulations** of the linearised model.

### Trial 1
- $K_p=20000$
- $K_i=5000$
- $K_d=50$
- Overshoot: about **248%**
- Settling time: about **4.9 s**
- Peak control deviation: about **$5.25 \times 10^4$ V**
- Verdict: **stable but unacceptable** because the overshoot is far too large.

### Trial 2
- $K_p=40000$
- $K_i=40000$
- $K_d=1500$
- Overshoot: about **75.7%**
- Settling time: about **2.0 s**
- Peak control deviation: about **$3.93 \times 10^4$ V**
- Verdict: **faster**, but still high overshoot and larger control demand.

### Trial 3 (selected)
- $K_p=32000$
- $K_i=20000$
- $K_d=1500$
- Overshoot: about **80.7%**
- Settling time: about **3.0 s**
- Peak control deviation: about **$3.12 \times 10^4$ V**
- Verdict: chosen as the **best overall compromise** among the PID trials considered.

## Selected controller

The final controller selected for the report is

$$
K_p=32000,\qquad K_i=20000,\qquad K_d=1500
$$

Hence,

$$
C(s)=32000+\frac{20000}{s}+1500s
=\frac{1500s^2+32000s+20000}{s}
$$

This was not the tuning with the smallest overshoot, but it gave the best balance between:
- BIBO stability,
- zero steady-state error,
- lower peak control deviation than the other improved design,
- and smoother behaviour than the original trial controller.

## Stability check for the selected controller

For the selected gains, the closed-loop characteristic polynomial is

$$
Q(s)=0.03s^5+456.1s^4+22478s^3+396870s^2+2.544\times 10^6 s+2.85\times 10^6
$$

The Routh first column is strictly positive:

$$
[0.03,\;456.1,\;22451.9,\;345194,\;2.358\times10^6,\;2.85\times10^6]
$$

so the Routh test indicates **no right-half-plane closed-loop poles**.

The direct root calculation gives approximately:

- $s_1 \approx -15153.95$
- $s_2 \approx -11.81$
- $s_{3,4} \approx -18.08 \pm 7.14j$
- $s_5 \approx -1.40$

All closed-loop poles lie in the open left half-plane, so the **linearised closed-loop system is BIBO stable**.

## Performance discussion

The selected controller gives an output that settles close to the reference with **negligible steady-state error**, which is consistent with the presence of integral action.

Its main weakness is the large overshoot (about **81%**) together with the large control demand. Even so, it is a substantial improvement over the first trial controller, and the response does not show sustained oscillation. The system rises, overshoots, and then returns smoothly to the setpoint.

The correct interpretation is that PID control provides a **compromise solution** for this plant. It stabilises the linearised model locally and removes offset, but it does not simultaneously optimise all performance measures. The final gains should therefore be presented as the **best compromise among the PID tunings tested**, not as a globally optimal controller.

## Practical limitations

There are two main practical limitations.

1. **Large voltage demand**  
   The equilibrium bias voltage is already very large because $R=2.2\,\text{k}\Omega$. The control deviation is also large, so the total applied voltage can become extremely high. This is an actuator limitation.

2. **Linearisation validity**  
   The controller was designed from the linearised model around $x_0=0.50\,\text{m}$. If the state moves far away from this operating point, the linear approximation may no longer be accurate.

Because of this, the report should state that **nonlinear validation** is required before claiming that the controller would work well in practice.
