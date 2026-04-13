# Mechanical model derivation (ball on incline)

## Coordinate system
- x: along the incline, **positive downhill**
- φ: incline angle (radians)
- States: x (position), v = ẋ (velocity)

## Forces along the incline (positive downhill)
- Gravity component: + m g sin(φ)
- Spring force: F_s = -k(x - d) (spring is unstretched at x = d)
- Viscous damper: F_d = -b ẋ
- Magnetic attraction toward magnet at x = δ:
  - distance y = δ - x  (assume x < δ in normal operation)
  - F_mag = + c i^2 / (δ - x)^2
- Static friction at contact: T (unknown, will be eliminated)

## Translational dynamics (Newton along incline)
m ẍ = m g sin(φ) - k(x - d) - b ẋ + c i^2/(δ - x)^2 - T

## Rotational dynamics about centre
I θ̈ = -T r   (friction causes clockwise torque; CCW is positive)

## Rolling constraint (assuming no slip)
ẍ = - r θ̈

Therefore:
T = (I / r^2) ẍ

## Combined translational dynamics → single ODE
(m + I/r^2) ẍ = m g sin(φ) - k(x - d) - b ẋ + c i^2/(δ - x)^2

For a solid sphere: I = (2/5) m r^2, so:
(7/5)m ẍ = m g sin(φ) - k(x - d) - b ẋ + c i^2/(δ - x)^2

## Final form
ẍ = (5/(7m)) [ m g sin(φ) - k(x - d) - b ẋ + c i^2/(δ - x)^2 ]

## State-space form
x1 = x
x2 = v = ẋ

ẋ1 = x2
ẋ2 = (5/(7m)) [ m g sin(φ) - k(x1 - d) - b x2 + c i^2/(δ - x1)^2 ]

## Assumptions
- Rolling without slipping
- Ball is a solid sphere (I = 2/5 m r^2)
- Spring and damper act along the incline
- Magnetic force acts along the incline toward x = δ
- Ignore air drag/rolling resistance
