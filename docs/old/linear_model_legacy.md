# ⚠️ Legacy File (Do Not Use)

This file was an earlier combined draft of the modelling and linearisation.

It is no longer used.

The updated, structured modelling workflow is now split across:

- nonlinear_model.md
- operating_point.md
- deviation_variables.md
- linearisation.md
- transfer_function.md

This file is kept only for reference.


## System Definition

The system consists of a ball rolling along an inclined surface under the influence of gravity, spring force, damping, and magnetic force from an electromagnet.

The input to the linearised mechanical subsystem is the small-signal current deviation about the operating point:
u(t) = i(t) - i0


The output of the linearised model is the small signal position deviation: 
y(t) = x(t) - x0

Note: distance to the magnet is given by:
y_dist(t) = δ - x(t)

## Variables 

- x(t) : position of the ball along the incline (m)
- v(t) : velocity of the ball (m/s)
- i(t) : current in the electromagnet (A) 
- y(t) : small signal output position
- x0 : operating point position
- i0 : operating point current
- u(t) : small signal input current
- R : resistance (Ω)
- L(x) : inductance (H)
- m : mass of the ball (kg)
- g : gravitational acceleration (m/s<sup>2</sup>)
- k : spring constant (N/m)
- b : damping coefficient (Ns/m)
- c : magnetic force constant
- δ : fixed distance reference (m)
- φ : incline angle (radians)
- d : spring rest position (m)

## Nonlinear Model 

The system is described by the following nonlinear differential equations. 
### Mechanical Subsystem 
The kinematic relationship between position and velocity is: 
dx/dt = v 

The mechanical dynamics of the system are given by: 
dv/dt = (5/(7m)) [ m g sin(φ) - k(x - d) - b v + (c i²) / (δ - x)² ]

### Electrical Subsystem
The electrical dynamics of the electromagnet are given by:
di/dt = (V - Ri) / L(x)

The inductance depends on position:
L(x) = L<sub>0</sub> + L<sub>1</sub> e<sup>-α(δ - x)</sup>

In the linearised mechanical model, the current is treated as the input to the system.

## State Variables

The system is represented using the following state variables: 
x1 = x - x0 (position deviation)
x2 = v (velocity deviation)

The input is: 
u = i - i0 (current deviation) 

The output is: 
y = x - x0 (position deviation)

The system can be written in state space form as:

- dx1/dt = x2
- dx2/dt = -2691.2 x1 - 16.08 x2 + 4.62 u 

y = x1

## Linearised Model

The nonlinear system is linearised about an operating point using a small signal approximation. 
The linear model represents small deviations about the operating point.
The system is expressed in state form such as:
dx/dt = A x + B u 
y = C x + D u

Where the matrices are A, B, C, D are given by:

A = 
[ 0       1
-2691.2       -16.08 ]

B = 
[ 0
4.62 ]

C =
[ 1  0 ]

D =
[ 0 ]

Matrix A describes the internal dynamics of the system. It defines how the state variables, like position and velocity influence each other over time. The terms in A represent the effects of stiffness and damping. 

Matrix B describes how the input (current deviation) affects the system. 

Matrix C defines how the output is related to the state variables. Here, the output is the position of the ball, so y = x1. 

Matrix D represents any direct effect of the input on the output. Since D = 0, there is no direct feedthrough from the input to the output. 

## Transfer Function
The transfer function is obtained from the state-space model using:
G(s) = C(sI - A)<sup>-1</sup>B + D

This transfer function relates the output position of the ball to the input current deviation:

G(s) = X(s) / I(s)

After using Python, I found the transfer function to be : 
G(s) = 4.62 / (s<sup>2</sup> + 16.08s + 2691.2)

## Poles 
The poles of the system are given by the eigenvalues of matrix A:

p1 = -8.04 + 51.25j 

p2 = -8.04 - 51.25j 

Since the poles of the system have negative real parts, this indicates that the system is stable. The presence of imaginary components shows that the system exhibits oscillatory behaviour. 
