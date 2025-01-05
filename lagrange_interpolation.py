import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange

# Given data points
x = np.array([1, 2, 3])
y = np.array([2, 3, 5])

# Calculate the Lagrange polynomial
polynomial = lagrange(x, y)

# Display the polynomial
print(f"The Lagrange polynomial is: {polynomial}")

# Plot the data points and the exact polynomial curve
x_vals = np.linspace(1, 3, 100)
y_vals = polynomial(x_vals)

plt.scatter(x, y, color='red', label='Data Points')
plt.plot(x_vals, y_vals, label=f'Lagrange Polynomial: {polynomial}', color='blue')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Lagrange Polynomial Interpolation')
plt.show()
