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

In calculus, derivatives like 
    
    𝑑𝑦𝑑𝑥

represent rates of change—how one variable changes in relation to another. 
But here: dx means "the deviation of x from its mean", not an infinitesimally 
small change. dy does the same for y. So this notation is from statistics, 
not calculus.

Where This Connects to Derivatives?
There is an interesting bridge, though! 

When you calculate things like: Slope of a regression line

    𝑚= ∑ 𝑑𝑥⋅𝑑𝑦 / ∑ 𝑑𝑥**2

You're essentially computing a kind of average rate of change based 
on deviations—similar in spirit to a derivative, but using finite 
differences instead of limits


Once you’ve calculated the slope m and intercept b, 
you can create the regression equation:

    𝑦^= 𝑚 ⋅ 𝑥 + 𝑏

Slope:
𝑚 = ∑( 𝑥𝑖 − 𝑥ˉ)( 𝑦𝑖 − 𝑦ˉ) / ∑( 𝑥𝑖 − 𝑥ˉ)**2

intercept:
𝑏 = 𝑦ˉ− 𝑚 ⋅ 𝑥

Where:

- 𝑦^(y_pred) is the predicted value of y for a given x.
- 𝑚 is the slope, showing how much y changes for each unit increase in x.
- 𝑏 is the y-intercept, or the value of y when x = 0.
"""
import numpy as np
import matplotlib.pyplot as plt

x = np.array([1,  2, 3,  4, 5,  6,])
y = np.array([1,  2, 3,  4, 5,  6,])

# 2. Calculate means
x_mean = np.mean(x)
y_mean = np.mean(y)

# 3. Calculate the slope (m) and intercept (b) manually
numerator = np.sum((x - x_mean) * (y - y_mean))
denominator = np.sum((x - x_mean) ** 2)
m = numerator / denominator
b = y_mean - m * x_mean

# 4. Build the regression line
y_pred = m * x + b

# 5. Make a prediction for a new x value
x_new = 7
y_new = m * x_new + b

print(f"Slope (m): {m:.10f}")
print(f"Intercept (b): {b:.10f}")
print(f"Predicted y values: {[f'{val:.10f}' for val in y_pred]}")
print(f"Prediction for x={x_new}: y={y_new:.10f}")

# 6. Visualize the result
plt.scatter(x, y, color='blue', label='Data points')
plt.plot(x, y_pred, color='red', label='Regression line')
plt.scatter(
    [x_new], [y_new], 
    color='green', 
    label=f'Prediction (x={x_new}) y={y_new:.2f}')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Step-by-step Linear Regression')
plt.legend()
plt.show()
