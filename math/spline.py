import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Generate the first quarter of the sine signal with more data points
x_quarter = np.linspace(0, np.pi / 4, 1000)
y_quarter = np.sin(x_quarter)

# Create a cubic spline interpolation of the first quarter
cs = CubicSpline(x_quarter, y_quarter)

# Generate the second quarter of the sine signal using the spline
x_half = np.linspace(0, np.pi / 2, 2000)
y_half = np.sin(x_half)
y_interpolated = cs(x_half[1000:])

# Combine the first quarter and the interpolated second quarter
y_combined = np.concatenate((y_quarter, y_interpolated))

# Print ten points from start to end from both signals
print("x-value    | Original Sine y-value | Interpolated y-value")
print("-------------------------------------------------------")
for i in np.linspace(0, len(x_half) - 1, 10, dtype=int):
    print(f"{x_half[i]:.4f}    | {y_half[i]:.4f}               | {y_combined[i]:.4f}")

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(x_half, y_half, label='Original Sine Signal', linestyle='--')
plt.plot(x_half[:1000], y_quarter, 'o', label='First Quarter Data Points')
plt.plot(x_half[1000:], y_interpolated, 'x', label='Interpolated Second Quarter')
plt.plot(x_half, y_combined, label='Combined Signal')
plt.legend()
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.title('Improved Spline Interpolation of the Second Quarter of a Sine Signal')

# Set the position of the plot window
manager = plt.get_current_fig_manager()
manager.window.wm_geometry("+0+600")  # (x, y)

plt.show()