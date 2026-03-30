import numpy as np
from scipy.signal import ss2tf

# Linearised mechanical subsystem matrices
A = np.array([
    [0.0, 1.0],
    [-2691.2, -16.08]
])

B = np.array([
    [0.0],
    [4.62]
])

C = np.array([
    [1.0, 0.0]
])

D = np.array([[0.0]])

# Sensor time constant
tau_m = 0.03

# Mechanical transfer function from state-space
num, den = ss2tf(A, B, C, D)

# ss2tf returns a 2D numerator array for SISO, so take first row
num = num[0]

print("Mechanical transfer function:")
print("Numerator:", num)
print("Denominator:", den)

# Mechanical poles
mech_poles = np.roots(den)
print("\nMechanical poles:")
print(mech_poles)

# Sensor transfer function H(s) = 1 / (tau_m s + 1)
sensor_num = np.array([1.0])
sensor_den = np.array([tau_m, 1.0])

print("\nSensor transfer function:")
print("Numerator:", sensor_num)
print("Denominator:", sensor_den)

# Full transfer function in series: G_total(s) = G(s) * H(s)
full_num = np.polymul(num, sensor_num)
full_den = np.polymul(den, sensor_den)

print("\nFull transfer function including sensor:")
print("Numerator:", full_num)
print("Denominator:", full_den)

# Full poles
full_poles = np.roots(full_den)
print("\nFull open-loop poles including sensor:")
print(full_poles)

# Stability conclusion
if np.all(np.real(full_poles) < 0):
    print("\nConclusion: The full open-loop system is BIBO stable.")
elif np.any(np.real(full_poles) > 0):
    print("\nConclusion: The full open-loop system is unstable.")
else:
    print("\nConclusion: The full open-loop system is marginally stable.")
