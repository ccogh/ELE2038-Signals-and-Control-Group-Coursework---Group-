## System Definition

The system consists of a ball rolling along an inclined surface under the influence of gravity, spring force, damping, and magnetic force from an electro magnet.

The input to the system is the current in the electromagnet:
u(t) = i(t)

The output of the system is the distance between the centre of the ball and the centre of the electromagnet:
y(t) = δ - x(t)

## Variables 

- x(t) : position of the ball along the incline (m)
- v(t) : velocity of the ball (m/s)
- i(t) : current in the electromagnet (A) 
- V(t) : input voltage (V)
- y(t) : distance between the centre of the ball and the centre of the electromagnet

- R : resistance (Ω)
- L(x) : inductance (H)
- m : mass of the ball (kg)
- g : gravitational acceleration (m/s)
- k : spring constant (N/m)
- b : damping coefficient (Ns/m)
- c : magnetic force constant
- δ : fixed distance reference (m)
- φ : incline angle (radians)
- d : spring rest position (m)

## Nonlinear Model 

The system is described by the following nonlinear differential equations. 

The kinematic relationship between position and velocity: 
dx/dt = v 

The mechanical dynamics of the system ar3e given by: 
dv/dt = (5/(7m)) [ m g sin(φ) - k(x - d) - b v + (c i²) / (δ - x)² ]

The electrical dynamics of the electromagnet are given by:
di/dt = (V - Ri) / L(x)



The inductance depends on position:
L(x) = L<sub>0</sub> + L<sub>1</sub> e<sup>-α(δ - x)</sup>

The output of the system is the distance between the ball and electromagnet: 
y =  δ - x 

## State Variables

The system is represented using the following state variables: 
x1 = x (position) 
x2 = v (velocity) 
x3 = i (current)

The system can be written in state space form as:

- dx1/dt =x2
- dx2/dt = (5/(7m)) [ m g sin(φ) - k(x1 - d) - b x2 + (c x3²) / (δ - x1)² ]
-  dx3/dt = (V -R x3) / L(x1)


y = δ - x1

## Linearised Model

The non linear system is linearised about an operating point using a small signal approximation. 
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

Matrix A describes the internal dynamics of the system. It defines how teh state variables, like position and velocity influence each other over time. The terms in A represent the effects of stiffness and damping. 

Matrix B describes how the input affects the system. In this case, the input voltage influences the acceleration of the ball through the electromagnetic force.

Matrix C defines how the output is related to the state variables. Here, the output is the position of the ball. 

Matrix D represents any direct effect of the input on the output. Since D = 0, there is no direct feedthrough from the input to the output. 

## Transfer Function
The transfer function is obtained from the state-space model using:
G(s) = C(sI - A)<sup>-1</sup>B + D

After using Python, I found the transfer function to be : 
G(s) = 4.62 / (s<sup>2</sup> + 16.08s +2691.2)

## Poles 
The poles of the system are given by the eigenvalues of matrix A:

p1 = -8.04 + 51.25j 

p2 = -8.04 - 51.25j 

Since the poles of the system have negative real parts, this indicates that the system is stable. The presence of imaginary components shows that the system exhibits oscillatory behaviour. 
