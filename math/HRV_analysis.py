import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define the sine function to fit the heart rate data
def sine_wave(x, A, B, C, D):
    return A * np.sin(B * x + C) + D

# Simulated heart rate variability data (10-second period)
time_points = np.linspace(0, 10, 10)  # 10 time samples (seconds)
heart_rate_points = 80 + 20 * np.sin(2 * np.pi * time_points / 10)  # Oscillating between 60-100 BPM

# Fit the sine function to the heart rate data
params, _ = curve_fit(sine_wave, time_points, heart_rate_points, p0=[20, 2 * np.pi / 10, 0, 80])

# Print the sine wave terms (A, B, C, D)
print("Sine wave model parameters for HRV:")
print(f"A (Amplitude) = {params[0]:.2f} BPM")
print(f"B (Frequency) = {params[1]:.4f} (rad/s)")
print(f"C (Phase Shift) = {params[2]:.4f} rad")
print(f"D (Baseline HR) = {params[3]:.2f} BPM")

# Generate interpolated heart rate values over a smoother time range
time_range = np.linspace(min(time_points), max(time_points), 100)  # 100 points over 10s
heart_rate_range = sine_wave(time_range, *params)  # Predicted HRV values

# Prepare the table with original and interpolated values
original_data = {'Time (s)': time_points, 'HR (Original)': heart_rate_points}
interpolated_data = {'Time (s)': time_range, 'HR (Interpolated)': heart_rate_range}

# Convert to DataFrames
df_original = pd.DataFrame(original_data)
df_interpolated = pd.DataFrame(interpolated_data)

# Find the nearest time values in the interpolated data
def find_nearest(x, x_range):
    return x_range[np.abs(x_range - x).argmin()]

df_original['HR (Interpolated)'] = df_original['Time (s)'].apply(lambda x: sine_wave(find_nearest(x, time_range), *params))

# Print the table
print("\nOriginal and interpolated HR values:")
print(df_original[['Time (s)', 'HR (Original)', 'HR (Interpolated)']].to_string(index=False))

# Plotting the original and interpolated HRV signals
plt.figure(figsize=(8, 6))
plt.plot(time_points, heart_rate_points, 'bo', label='Original HR Data (BPM)', markersize=8)  # Original points
plt.plot(time_range, heart_rate_range, 'r-', label='Interpolated HRV Model')  # Interpolated sine curve
plt.xlabel('Time (s)')
plt.ylabel('Heart Rate (BPM)')
plt.title('Heart Rate Variability (HRV) Analysis')
plt.legend()
plt.grid(True)
plt.show()
