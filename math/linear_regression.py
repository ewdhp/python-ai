import numpy as np
import time
import matplotlib.pyplot as plt

# Using the model to make predictions
def predict(X):
    return m * X + b

# Start the timer
start_time = time.time()

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





X_new = 6
y_pred = predict(X_new)


# Stop the timer and calculate the elapsed time
end_time = time.time()
elapsed_time = (end_time - start_time) * 1000  

print(f"Calculated slope (m): {m}")
print(f"Calculated intercept (b): {b}")
print(f"Predicted value for X_new = 6: {y_pred}")
print(f"Elapsed time: {elapsed_time:.2f} ms")


