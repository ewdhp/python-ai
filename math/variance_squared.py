"""
Variance and Squared Deviations Visualization

This script demonstrates how (x - mean)^2 is calculated for each data point,
shows a table, and plots the squared deviations visually.
"""
import numpy as np
import matplotlib.pyplot as plt

# Example data
data = np.array([2, 4, 5, 4, 5])
mean = np.mean(data)

print(f"Data: {data}")
print(f"Mean: {mean}")

print("\nTable of squared deviations:")
print(f"{'x':>3} {'x-mean':>8} {'(x-mean)^2':>12}")
for xi in data:
    dx = xi - mean
    dx2 = dx ** 2
    print(f"{xi:>3} {dx:>8.2f} {dx2:>12.2f}")

# Plot the data, mean, and squared deviations
plt.figure(figsize=(8, 5))
plt.scatter(range(len(data)), data, color='blue', label='Data points')
plt.axhline(mean, color='red', linestyle='--', label='Mean')

for i, xi in enumerate(data):
    plt.plot([i, i], [mean, xi], color='gray', linestyle=':')
    plt.text(i, (xi + mean) / 2, f"{(xi-mean)**2:.2f}", color='purple', ha='center')

plt.title('Squared Deviations from the Mean')
plt.xlabel('Index')
plt.ylabel('Value')
plt.legend()
plt.tight_layout()
plt.show()
