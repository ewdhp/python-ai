import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge

# Step 1: Generate random sunlight hours (between 2 to 12 hours per day)
np.random.seed(42)  # For reproducibility
sunlight_hours = np.sort(np.random.uniform(2, 12, 15))  # 15 random values between 2 and 12 hours

# Step 2: Define a linear trend (without noise)
true_slope = 5.5  # True slope of the growth trend
true_intercept = 8  # Base plant height at 0 sunlight hours

# Step 3: Add random noise to simulate variability in the data
noise = np.random.normal(0, 15, size=sunlight_hours.shape)  # Gaussian noise with mean=0 and std=15

# Step 4: Generate observed plant heights by combining trend + noise
plant_height = true_intercept + true_slope * sunlight_hours + noise

# Step 5: Apply Ridge Regression (Regularization)
ridge_model = Ridge(alpha=1.0)  # The 'alpha' is the regularization strength
sunlight_hours_reshaped = sunlight_hours.reshape(-1, 1)  # Reshape for sklearn input format
ridge_model.fit(sunlight_hours_reshaped, plant_height)

# Step 6: Predict the plant height based on the fitted Ridge model
predicted_plant_height_ridge = ridge_model.predict(sunlight_hours_reshaped)

# Step 7: Calculate residuals (Observed - Predicted)
residuals = plant_height - predicted_plant_height_ridge

# Step 8: Plotting the results
plt.figure(figsize=(8, 6))
plt.scatter(sunlight_hours, plant_height, color='blue', label="Observed Data", s=80)
plt.plot(sunlight_hours, predicted_plant_height_ridge, color='red', label="Ridge Regression (Detected Pattern)")

# Plot the residuals
plt.scatter(sunlight_hours, residuals, color='green', label="Residuals", zorder=5)

# Plot the predicted points for the next hours (using the Ridge model)
next_sunlight_hours = np.array([sunlight_hours[-1] + i for i in range(1, 6)])  # Next 5 hours after the last one
next_sunlight_hours_reshaped = next_sunlight_hours.reshape(-1, 1)
predicted_plant_height_with_noise = ridge_model.predict(next_sunlight_hours_reshaped) + np.random.normal(0, 15, size=next_sunlight_hours.shape)

plt.scatter(next_sunlight_hours, predicted_plant_height_with_noise, color='orange', marker='x', s=100, label="Predicted Growth (With Noise)")

plt.xlabel("Sunlight (hours/day)")
plt.ylabel("Plant Height (cm)")
plt.title("Observed Plant Growth with Ridge Regression and Residuals")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

# Print residuals
print("Residuals (Observed - Predicted):")
for i, (observed, predicted, residual) in enumerate(zip(plant_height, predicted_plant_height_ridge, residuals)):
    print(f"Sunlight: {sunlight_hours[i]:.2f} hours → Observed: {observed:.2f} cm, Predicted: {predicted:.2f} cm, Residual: {residual:.2f} cm")
