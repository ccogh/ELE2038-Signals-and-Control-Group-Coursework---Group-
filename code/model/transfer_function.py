import control as ctrl

# Define Laplace variable
s = ctrl.TransferFunction.s

# Mechanical transfer function
G = 4.62 / (s**2 + 16.08*s + 2691.2)

# Sensor transfer function
tau_m = 0.03
H = 1 / (tau_m*s + 1)

# Full transfer function including sensor
G_total = G * H

print("Mechanical transfer function:")
print(G)

print("\nFull transfer function including sensor:")
print(G_total)

print("\nMechanical poles:")
print(ctrl.poles(G))

print("\nFull system poles:")
print(ctrl.poles(G_total))
