"""
Step-by-step Linear Regression Example


This script demonstrates linear regression 
with a small dataset, showing each step:

1. Data collection
2. Calculating means
3. Calculating the slope (m) and intercept (b)
4. Building the regression line
5. Making predictions
6. Visualizing the result

Great question! Here’s what the numerator and denominator represent 
in the context of linear regression:

Numerator
numerator = Σ((x_i - x̄) * (y_i - ȳ))

This is the sum of the products of the deviations of x and y 
from their means. It measures how much x and y vary together (covariance).
In the table, this is the sum of the (x-x̄)*(y-ȳ) column.
Geometrically, it tells you if the points tend to go up together (positive),
down together (positive), or in opposite directions (negative).

Denominator
denominator = Σ((x_i - x̄)^2)

This is the sum of the squared deviations of x from its mean.
It measures how much x varies by itself (variance of x).

In the table, this is the sum of the (x-x̄)^2 column.

Slope (m)
m = numerator / denominator

The slope is the ratio of how much y changes with x, normalized 
by how much x varies.

The “straight line at the middle” is the regression line, which 
is determined by this slope and the intercept.
Summary:

- The numerator is the sum of the products of deviations (covariance).
- The denominator is the sum of squared deviations of x (variance).

Their ratio gives the slope of the best-fit line.

---------------------------
Variance measures how spread out a set of numbers is. It tells you how 
much the values in a dataset differ from the mean (average) of the dataset.

Interpretation:
A low variance means the data points are close to the mean.
A high variance means the data points are more spread out.

"""
import numpy as np
import matplotlib.pyplot as plt

# 1. Data collection
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])

# 2. Calculate means
x_mean = np.mean(x)
y_mean = np.mean(y)
print(f"Mean of x: {x_mean}")
print(f"Mean of y: {y_mean}")

# 3. Calculate the slope (m) and intercept (b) manually
print("\nTable for slope calculation:")
print(f"{'x':>3} {'y':>3} {'x-x̄':>8} {'y-ȳ':>8} {'(x-x̄)*(y-ȳ)':>15} {'(x-x̄)^2':>10}")
for xi, yi in zip(x, y):
    dx = xi - x_mean
    dy = yi - y_mean
    prod = dx * dy
    dx2 = dx ** 2
    print(f"{xi:>3} {yi:>3} {dx:>8.2f} {dy:>8.2f} {prod:>15.2f} {dx2:>10.2f}")

numerator = np.sum((x - x_mean) * (y - y_mean))
denominator = np.sum((x - x_mean) ** 2)
m = numerator / denominator
b = y_mean - m * x_mean

print(f"Slope (m): {m}")
print(f"Intercept (b): {b}")

# 4. Build the regression line
y_pred = m * x + b
print(f"Predicted y values: {y_pred}")

# 5. Make a prediction for a new x value
x_new = 6
y_new = m * x_new + b
print(f"Prediction for x={x_new}: y={y_new}")

# 6. Visualize the result
plt.scatter(x, y, color='blue', label='Data points')
plt.plot(x, y_pred, color='red', label='Regression line')
plt.scatter([x_new], [y_new], color='green', label=f'Prediction (x={x_new})')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Step-by-step Linear Regression')
plt.legend()
plt.show()
