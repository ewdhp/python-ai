"""
The curve_fit function from scipy.optimize uses the Levenberg-Marquardt 
algorithm by default, which is a combination of the Gauss-Newton algorithm 
and gradient descent. It's often used for non-linear least squares curve fitting.

Key Points about Levenberg-Marquardt:
Purpose: It's designed to minimize the sum of the squared residuals 
(the differences between observed data and the model's predictions).
Adaptability: It blends the Gauss-Newton algorithm, which is efficient 
when the model is close to linear, and gradient descent, which helps when 
the problem is more non-linear.

Efficiency: This hybrid approach allows the algorithm to perform well in 
a variety of situations, especially when dealing with non-linear models 
like the sine wave.

You can also specify other methods for optimization in curve_fit, such as:

- Trust Region Reflective (trf)
- Dogbox (dogbox)
- Powell (powell)

These are more general optimization techniques and might be used for 
specific problem characteristics. However, for most standard curve-fitting 
problems, the default Levenberg-Marquardt works very well.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Example set of points (x, y) representing one complete sine cycle
x_points = np.linspace(0, 2 * np.pi, 10)  # 10 points in one sine cycle
y_points = np.sin(x_points)  # The y values are the sine of the x values

# Define the sine function to fit
def sine_wave(x, A, B, C, D):
    return A * np.sin(B * x + C) + D

# Fit the data to the sine model
params, _ = curve_fit(sine_wave, x_points, y_points, p0=[1, 1, 0, 0])

# Print the sine wave terms (A, B, C, D)
print("Sine wave terms:")
print(f"A = {params[0]}")
print(f"B = {params[1]}")
print(f"C = {params[2]}")
print(f"D = {params[3]}")

# Generate terms for the sine wave (we'll generate for a range of x values)
x_range = np.linspace(min(x_points), max(x_points), 100)  # Range of x values with 100 points
y_range = sine_wave(x_range, *params)  # Corresponding y values based on the sine wave

# Prepare the table with original and interpolated values
original_data = {'x': x_points, 'y (Original)': y_points}
interpolated_data = {'x': x_range, 'y (Interpolated)': y_range}

# Convert to DataFrames
df_original = pd.DataFrame(original_data)
df_interpolated = pd.DataFrame(interpolated_data)

# Find the nearest x values in the interpolated data
def find_nearest(x, x_range):
    return x_range[np.abs(x_range - x).argmin()]

df_original['y (Interpolated)'] = df_original['x'].apply(lambda x: sine_wave(find_nearest(x, x_range), *params))

# Print the table
print("\nOriginal and interpolated values:")
print(df_original[['x', 'y (Original)', 'y (Interpolated)']].to_string(index=False))

# Plotting the original and interpolated signals
plt.figure(figsize=(8, 6))
plt.plot(x_points, y_points, 'bo', label='Original Data (x, sin(x))', markersize=8)  # Original points
plt.plot(x_range, y_range, 'r-', label='Interpolated Sine Wave')  # Interpolated sine curve
plt.xlabel('x')
plt.ylabel('y')
plt.title('Original Data and Interpolated Sine Wave')
plt.legend()
plt.grid(True)
plt.show()
