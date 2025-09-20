# Animated demonstration of superposition and interference of two waves
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Wave parameters
A1 = 1.0      # Amplitude of wave 1
A2 = 1.0      # Amplitude of wave 2
lambda_ = 1.0 # Wavelength
k =  np.pi / lambda_  # Wave number
omega = 2 * np.pi / 2.0  # Angular frequency

# Spatial domain
x = np.linspace(0, 4 * lambda_, 500)

# Phase difference (can be changed to see constructive/destructive)
phase_diff = 0#np.pi  # Try 0 for constructive, pi for destructive

# Gaussian window parameters
center1 = 3*lambda_      # Center of wave 1
center2 = 3 * lambda_  # Center of wave 2
sigma = 0.4 * lambda_  # Width of the window

# Gaussian window functions
window1 = np.exp(-((x - center1) ** 2) / (2 * sigma ** 2))
window2 = np.exp(-((x - center2) ** 2) / (2 * sigma ** 2))

# Set up plot
fig, ax = plt.subplots(figsize=(8, 4))
line1, = ax.plot([], [], 'b-', label='Wave 1')
line2, = ax.plot([], [], 'r-', label='Wave 2')
line_sum, = ax.plot([], [], 'k-', label='Superposition')
ax.set_xlim(x[0], x[-1])
ax.set_ylim(-2.2, 2.2)
ax.set_xlabel('Position')
ax.set_ylabel('Amplitude')
ax.set_title('Superposition and Interference of Two Waves')
ax.legend()

def init():
	line1.set_data([], [])
	line2.set_data([], [])
	line_sum.set_data([], [])
	return line1, line2, line_sum

def animate(t):
	# Apply Gaussian windowing to each wave
	y1 = A1 * np.sin(k * x - omega * t) * window1  # Wave 1 with window
	y2 = A2 * np.sin(k * x - omega * t + phase_diff) * window2  # Wave 2 with window
	y_sum = y1 + y2  # Superposition
	line1.set_data(x, y1)
	line2.set_data(x, y2)
	line_sum.set_data(x, y_sum)
	return line1, line2, line_sum

ani = FuncAnimation(fig, animate, frames=np.linspace(0, 4 * np.pi, 120), init_func=init,
					blit=True, interval=50, repeat=True)


# --- Frequency domain analysis (spectrum) ---
# Compute the spectrum of the superposed wave at a fixed time (e.g., t=0)
y1_static = A1 * np.sin(k * x) * window1
y2_static = A2 * np.sin(k * x + phase_diff) * window2
y_sum_static = y1_static + y2_static

# Compute FFT
Y = np.fft.fft(y_sum_static)
freq = np.fft.fftfreq(len(x), d=(x[1] - x[0]))

# Plot spectrum
plt.figure(figsize=(8, 4))
plt.plot(freq, np.abs(Y), 'k-')
plt.title('Frequency Spectrum of Superposed Wave')
plt.xlabel('Spatial Frequency (1/units of x)')
plt.ylabel('Magnitude')
plt.xlim(0, np.max(freq))  # Show only positive frequencies
plt.grid(True)
plt.tight_layout()
plt.show()

