import numpy as np
import matplotlib.pyplot as plt

# Given data points
x = np.array([1, 2, 3, 4])
y = np.array([2, 3, 5, 10])

# Fit a polynomial of degree 2 (quadratic)
coefficients = np.polyfit(x, y, 2)

# Create the polynomial function using the coefficients
polynomial = np.poly1d(coefficients)

# Display the polynomial equation
print(f"The fitted polynomial is: {polynomial}")

# Plot the data points and the fitted polynomial curve
x_vals = np.linspace(1, 4, 100)  # Generate more points for smooth plotting
y_vals = polynomial(x_vals)

plt.scatter(x, y, color='red', label='Data Points')  # Plot the original data
plt.plot(x_vals, y_vals, label=f'Fitted Polynomial: {polynomial}', color='blue')  # Plot the fitted polynomial curve
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Polynomial Fit')
plt.show()
