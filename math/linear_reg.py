import numpy as np
import matplotlib.pyplot as plt

# Sample data: Sunlight hours and plant height
sunlight_hours = np.array([2, 4, 6, 8, 10, 12])
plant_height = np.array([15, 25, 40, 50, 65, 80])

# Compute means
X_mean = np.mean(sunlight_hours)
Y_mean = np.mean(plant_height)

# Compute beta1 (slope)
numerator = np.sum((sunlight_hours - X_mean) * (plant_height - Y_mean))
denominator = np.sum((sunlight_hours - X_mean) ** 2)
beta1 = numerator / denominator

# Compute beta0 (intercept)
beta0 = Y_mean - (beta1 * X_mean)

# Predict Y values for existing sunlight hours
Y_pred = beta0 + beta1 * sunlight_hours

# Generate 5 future predictions (next 5 sunlight hours)
future_sunlight_hours = np.array([14, 16, 18, 20, 22])
future_predictions = beta0 + beta1 * future_sunlight_hours

# Plot data points and regression line
plt.scatter(sunlight_hours, plant_height, color='blue', label="Observed Data", s=80)
plt.plot(sunlight_hours, Y_pred, color='red', label="Regression Line")

# Plot future predictions
plt.scatter(future_sunlight_hours, future_predictions, color='green', marker='x', s=100, label="Predicted Growth")

plt.xlabel("Sunlight (hours/day)")
plt.ylabel("Plant Height (cm)")
plt.title("Plant Growth vs. Sunlight Exposure (With Predictions)")
plt.legend()
plt.grid(True)

# Move the plot to the bottom-left corner (for Tkinter-based Matplotlib backends)
manager = plt.get_current_fig_manager()
try:
    manager.window.setGeometry(0, 800, 800, 600)  # (x, y, width, height)
except AttributeError:
    print("Warning: This feature may not work in some environments.")

# Show the plot
plt.show()

# Print predictions
print(f"Intercept (β₀): {beta0:.2f}")
print(f"Slope (β₁): {beta1:.2f}\n")
for i, (x, y) in enumerate(zip(future_sunlight_hours, future_predictions), 1):
    print(f"Prediction {i}: Sunlight {x} hours → Plant Height {y:.2f} cm")
