import control as ctrl
import numpy as np

# Define Laplace variable
s = ctrl.TransferFunction.s

# Mechanical transfer function (from linearisation)
G = 4.62 / (s**2 + 16.08*s + 2691.2)

# Sensor transfer function
tau_m = 0.03
H = 1 / (tau_m*s + 1)

# Full system (sensor in series)
G_total = G * H

print("Mechanical transfer function:")
print(G)

print("\nFull transfer function including sensor:")
print(G_total)

# Get poles
mech_poles = ctrl.poles(G)
full_poles = ctrl.poles(G_total)

print("\nMechanical poles:")
print(mech_poles)

print("\nFull system poles:")
print(full_poles)

# Simple stability check
if np.all(np.real(full_poles) < 0):
    print("\nSystem is BIBO stable")
elif np.any(np.real(full_poles) > 0):
    print("\nSystem is unstable")
else:
    print("\nSystem is marginally stable")

# Optional (not required but useful for later)
# t, y = ctrl.step_response(G_total)
