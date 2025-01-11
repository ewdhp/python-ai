import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Set the backend to 'TkAgg' (for interactive plotting)
matplotlib.use('TkAgg')

# Example data
y_true = np.array([3, -0.5, 2, 7])  # True values
y_pred = np.array([2.5, 0.0, 2, 8])  # Predicted values

# Calculate Mean Squared Error (MSE)
msg = np.mean((y_true - y_pred) ** 2)
print(f"Mean Squared Error: {msg}")

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(y_true, label="True values", marker='o', linestyle='-', color='b')
plt.plot(y_pred, label="Predicted values", marker='x', linestyle='--', color='r')
plt.title("True vs Predicted Values")
plt.xlabel("Index")
plt.ylabel("Value")
plt.legend()
plt.grid(True)

# Show the plot interactively (will pop up a window with the plot)
plt.show()
