## System Definition

The system consists of a ball rolling along an inclined surface under the influence of gravity, spring force, damping, and magnetic force from an electro magnet.

The input to the system is the voltage applied to the electromagnet coil:
u(t0 = V(t)

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
x3 = i (
