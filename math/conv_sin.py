import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve

# Define parameters
fs = 1000  # Sampling frequency
T = 2      # Total time duration
omega = 2 * np.pi * 5  # Frequency of sine wave (5 Hz)

t = np.linspace(-T, T, 2 * fs, endpoint=False)  # Time vector
signal = np.sin(omega * t)  # Sine wave signal

# Compute convolution
conv_result = convolve(signal, signal, mode='same') / fs  # Normalize by sampling rate

# Theoretical approximation: (t/2) * sin(omega*t)
theoretical = (t / 2) * np.sin(omega * t)

# Plot results
plt.figure(figsize=(10, 5))
plt.plot(t, conv_result, label='Convolution Result', linewidth=2)
plt.plot(t, theoretical, '--', label='Theoretical: (t/2) * sin(omega t)', linewidth=2)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Convolution of Two Identical Sine Waves')
plt.legend()
plt.grid()
plt.show()