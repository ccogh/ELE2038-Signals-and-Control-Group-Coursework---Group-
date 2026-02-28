import numpy as np 
from scipy.signal import ss2tf 

# Define matrices
A = np.array([
    [0, 1],
    [-2691.2, -16.08]
])

B = np.array([
 [0],
 [4.62]
])

C = np.array([
    [1, 0]
])

D = np.array([[0]])

# Transfer function
num, den = ss2tf(A, B ,C, D) 

print("Numerator:", num)
print("Denominator:", den )

# Poles
poles = np.linalg.eigvals(A)

print("Poles:", poles)

