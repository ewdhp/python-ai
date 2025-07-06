"""
Linear Regression and the Tangent

Suppose you have a set of data points and you want to fit a straight line 
(linear regression). The slope of the best-fit line is often denoted as "m". 
If you interpret the slope as the tangent of an angle θ (i.e., m = tan(θ)), then:

θ = arctan(m)

This angle θ represents the inclination of the regression line 
with respect to the x-axis.

Steps in the Process

Collect Data: Gather pairs of (x, y) data points.
Fit a Line: Use least squares regression to find the best-fit line, y = mx + b.
Calculate the Slope: The slope m is calculated as:
Find the Angle: Compute θ = arctan(m).

Interpretation: 
    The tangent (tan(θ)) gives the rate of change of y with respect to x.

The angle θ can be useful for interpreting the steepness of the relationship.
In some statistical visualizations, the angle of a trend line is more 
intuitive than the slope.

In circular statistics (dealing with angles), the tangent function is used to 
transform between linear and angular representations.

Summary:
The tangent function in statistics is often used to interpret 
the slope of a line as an angle, which can provide geometric 
insight into the relationship between variables.
"""
import numpy as np

# Example data
x = np.array([1, 2, 3, 4])
y = np.array([2, 3, 5, 7])

# Linear regression
m, b = np.polyfit(x, y, 1)

# Angle in radians and degrees
theta = np.arctan(m)
theta_deg = np.degrees(theta)

print(f"Slope: {m}")
print(f"Angle (radians): {theta}")
print(f"Angle (degrees): {theta_deg}")
