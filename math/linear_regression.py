import numpy as np

# Sample data
X = np.array([1, 2, 3, 4, 5])
y = np.array([1.2, 1.9, 3.0, 3.9, 5.1])

# Step 1: Calculate the means of X and y
X_mean = np.mean(X)
y_mean = np.mean(y)

# Step 2: Calculate the slope (m)
numerator = sum((X - X_mean) * (y - y_mean))
denominator = sum((X - X_mean) ** 2)
m = numerator / denominator

# Step 3: Calculate the intercept (b)
b = y_mean - m * X_mean

print(f"Calculated slope (m): {m}")
print(f"Calculated intercept (b): {b}")

# Using the model to make predictions
def predict(X):
    return m * X + b

X_new = 6
y_pred = predict(X_new)
print(f"Predicted value for X_new = 6: {y_pred}")

# Optional: Plotting the data and the linear model
import matplotlib.pyplot as plt

plt.scatter(X, y, color='blue', label='Data points')
plt.plot(X, predict(X), color='red', label='Linear model')
plt.xlabel('X')
plt.ylabel('y')
plt.legend()
plt.show()
