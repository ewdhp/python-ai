import numpy as np
import pandas as pd
from numpy.polynomial.polynomial import Polynomial

# Example set of points (x, y)
points = [(0, 1), (1, 3), (2, 7), (3, 13)]  # Example data (x, y)

# Separate the x and y values
x_points, y_points = zip(*points)

# Fit a polynomial to the points (degree will be len(points)-1 for exact fit)
degree = len(points) - 1
polynomial = Polynomial.fit(x_points, y_points, degree)

# Print the polynomial terms
print("Polynomial terms (in standard form):")
for i, coeff in enumerate(polynomial.coef):
    print(f"x^{i}: {coeff}")

# Generate terms for the series (we'll generate for a range of x values)
x_range = np.linspace(min(x_points), max(x_points), 10)  # Range of x values with 10 points
y_range = polynomial(x_range)  # Corresponding y values based on the polynomial

# Prepare the table with original and interpolated values
original_data = {'x': x_points, 'y (Original)': y_points}
interpolated_data = {'x': x_range, 'y (Interpolated)': y_range}

# Convert to DataFrames
df_original = pd.DataFrame(original_data)
df_interpolated = pd.DataFrame(interpolated_data)

# Find the nearest x values in the interpolated data
def find_nearest(x, x_range):
    return x_range[np.abs(x_range - x).argmin()]

df_original['y (Interpolated)'] = df_original['x'].apply(lambda x: polynomial(find_nearest(x, x_range)))

# Print the table
print("\nOriginal and interpolated values:")
print(df_original[['x', 'y (Original)', 'y (Interpolated)']].to_string(index=False))
