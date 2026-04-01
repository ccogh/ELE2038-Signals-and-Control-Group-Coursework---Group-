import control as ctrl
import numpy as np

# Make NumPy output easier to read
np.set_printoptions(precision=3, suppress=True)

# Linearised 3-state plant matrices
A = np.array([
    [0.0, 1.0, 0.0],
    [133.0, -16.08, 20.68],
    [0.0, 0.0, -15158.82]
])

B = np.array([
    [0.0],
    [0.0],
    [6.89]
])

C = np.array([
    [1.0, 0.0, 0.0]
])

D = np.array([
    [0.0]
])

# Create state-space plant
plant_ss = ctrl.ss(A, B, C, D)

# Convert plant to transfer function
G = ctrl.tf(plant_ss)

# Sensor transfer function
tau_m = 0.03
s = ctrl.TransferFunction.s
H = 1 / (tau_m * s + 1)

# Full system (plant + sensor)
G_total = G * H

# Round transfer function coefficients so printout looks nicer
G = ctrl.tf(np.round(G.num[0][0], 3), np.round(G.den[0][0], 3))
G_total = ctrl.tf(np.round(G_total.num[0][0], 3), np.round(G_total.den[0][0], 3))

print("Plant transfer function (Voltage -> Position):")
print(G)

print("\nFull transfer function including sensor:")
print(G_total)

# Get poles
plant_poles = ctrl.poles(G)
full_poles = ctrl.poles(G_total)

print("\nPlant poles:")
print(np.round(plant_poles, 3))

print("\nFull system poles:")
print(np.round(full_poles, 3))

# Stability check
if np.all(np.real(full_poles) < 0):
    print("\nFull system is BIBO stable")
elif np.any(np.real(full_poles) > 0):
    print("\nFull system is unstable")
else:
    print("\nFull system is marginally stable")

# Optional for later
# t, y = ctrl.step_response(G_total)
