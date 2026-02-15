# Electrical and Sensor Modelling

The aim of this section is to derive the electrical circuit dynamics of the electromagnet and the measurement equation for the sensor. 


## Variables

- \(x(t)\): position of the ball (m)
- \(y(t)\): distance from the electromagnet (m)
- \(i(t)\): current in the circuit (A)
- \(V(t)\): input voltage (V)
- \(R\): resistance (Ω)
- \(L\): inductance (H)
- \(y<sub>m</sub>(t)\): measured position (sensor output)


The distance between the ball and the electromagnet is given by: 

y(t) = δ - x(t)


The electromagentic force depends on the distance \(y\), not directly on the position \(x\).


## Inductance model

The inductance of the electromagnet varies with distance and is given by: 

L(x) = L<sub>0</sub> + L<sub>1</sub> e<sup>-α(δ - x)</sup>

This shows that the inductance changes as the ball moves, making the system nonlinear. 


## Electrical Model

Applying Kirchhoff's Voltage Law (KVL) to the circuit:

V(t) = R i(t) + d/dt (L(x) i(t))


where \(R i(t)\) is the voltage across the resistor and the inductor voltage is given by \(v<sub>L</sub> = d/dt (Li)\)

Since the inductance depends on position, the product rule must be applied when differentiating: 

d/dt(L i) = L(x) di/dt + i(t) dL/dt


Substituting gives: 

V(t) = R i (t) + L(x) di/dt + i(t) dL/dt




To simplify the model, the following assumption is made:

**Assumption A1:** The term i(t) dL/dt\) is neglected to simplify the model and avoid coupling with the mechanical dynamics.

This gives: 

V(t) ≈ Ri(t) + L(x) di/dt




Rearranging:

L(x) di/dt  = V(t) - R i(t)



di/dt = (V(t) - R i(t)) / L(x)


This is the electrical state equation.


## Sensor Model 

The sensor is modelled as a first-order system with time constant \(τ<sub>m</sub>\). Let the sensor output be \(y<sub>m</sub>(t)\).


τ<sub>m</sub> dy<sub>m</sub>/dt + y<sub>m</sub> = K<sub>m</sub> x(t)



Rearranging: 

dy<sub>m</sub>/dt = (K<sub>m</sub> x(t) - y<sub>m</sub>(t))/τ<sub>m</sub>


The sensor gain is assumed to be 1:

**Assumption A2:** \(K<sub>m</sub> = 1\)

So:

dy<sub>m</sub>/dt = x((t) - y<sub>m</sub>(t)) / τ<sub>m</sub>


This is the sensor model.

The measured output of the system is taken as: 

y = y<sub>m</sub> 

The sensor output can be written as:

y = K<sub>m</sub> x


