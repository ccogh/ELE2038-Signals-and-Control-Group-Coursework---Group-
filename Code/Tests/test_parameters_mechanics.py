import math
from mechanics import MechParams, accel, mech_rhs

p = MechParams(
    m=0.462,
    g=9.81,
    phi=math.radians(41.0),
    k=1885.0,
    b=10.4,
    d=0.42,
    c=6.811e-3,   #converted g -> approx. kg
    delta=0.65,
    r=0.123
)

#example: evaluating acceleration at the setpoint
x0 = 0.40
v0 = 0.0

print("accel @ i=0 A:", accel(x0, v0, i=0.0, p=p))
print("accel @ i=0.1 A:", accel(x0, v0, i=0.1, p=p))
print("RHS:", mech_rhs(0.0, (x0, v0), i=0.1, p=p))
