"""
This script defines the function f(x) = x^3 - 2x^2 + x - 5 and computes 
its gradient (derivative) numerically using the central difference method.
The results are displayed in a formatted table and plotted for visualization.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the function
def f(x):
    return x**3 - 2*x**2 + x - 5

# Calculate the gradient numerically
def numerical_gradient(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

# Generate x values
x_values = np.linspace(-5, 5, 21)
y_values = f(x_values)
grad_values = numerical_gradient(f, x_values)

# Create a formatted table using pandas
df = pd.DataFrame({
    'x': x_values,
    'f(x)': y_values,
    "f'(x)": grad_values
})
print(df.to_string(index=False, float_format="%.4f"))

# Plot the function and its gradient
plt.figure(figsize=(10, 6))
plt.plot(x_values, y_values, label='f(x)', marker='o')
plt.plot(x_values, grad_values, label="f'(x) (gradient)", marker='x')
plt.title('Function and its Gradient')
plt.xlabel('x')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.show()
