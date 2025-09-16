import numpy as np
import matplotlib.pyplot as plt

# Parameters
wavelength = 500e-9   # 500 nm (green light)
d = 5e-6              # slit separation = 5 micrometers
L = 1.0               # distance to screen = 1 meter
I0 = 1.0              # max intensity

# Screen setup
x = np.linspace(-0.02, 0.02, 2000)  # screen positions (±2 cm)
theta = np.arctan(x / L)            # angle approximation

# Interference pattern (no single-slit diffraction for simplicity)
I = I0 * np.cos(np.pi * d * np.sin(theta) / wavelength)**2

# Normalize for plotting
I /= np.max(I)

# Plot
plt.figure(figsize=(8,4))
plt.plot(x*1000, I, color='blue')
plt.title("Young's Double-Slit Interference Pattern")
plt.xlabel("Screen position (mm)")
plt.ylabel("Normalized Intensity")
plt.grid(alpha=0.3)
plt.show()
