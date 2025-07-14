"""
Gradient Descent for Linear Regression: Minimizing the Sum of Squared Errors (SSE)

This script demonstrates how to fit a line y = mx + b to data by minimizing the sum of squared errors using gradient descent.
"""
import numpy as np
import matplotlib.pyplot as plt

# Example data (noisy linear)
x = np.array([1, 2, 3, 4, 5])
y = np.array([2.1, 4.0, 6.1, 8.2, 10.1])

# Initialize parameters
m = 0.0
b = 0.0
learning_rate = 0.01
n_epochs = 1000
n = len(x)

# Gradient Descent
for epoch in range(n_epochs):
    y_pred = m * x + b
    error = y_pred - y
    sse = np.sum(error ** 2)
    # Gradients
    dm = (2/n) * np.sum(error * x)
    db = (2/n) * np.sum(error)
    # Update
    m -= learning_rate * dm
    b -= learning_rate * db
    if epoch % 100 == 0:
        print(f"Epoch {epoch}: SSE={sse:.4f}, m={m:.4f}, b={b:.4f}")

print(f"Final parameters: m={m:.4f}, b={b:.4f}")

# Plot
plt.scatter(x, y, color='blue', label='Data')
plt.plot(x, m * x + b, color='red', label='Fitted line')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Linear Regression via Gradient Descent (SSE Minimization)')
plt.legend()
plt.show()
