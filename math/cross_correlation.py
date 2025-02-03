import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate

# Create two signals: one is a noisy sine wave and the other is a smaller signal
# that is a sine wave pattern we want to detect in the larger signal.

# Signal 1: Noisy sine wave
t = np.linspace(0, 1, 1000, endpoint=False)
signal_1 = np.sin(2 * np.pi * 5 * t) + 0.5 * np.random.randn(1000)  # Adding noise

# Signal 2: A smaller sine wave pattern
signal_2 = np.sin(2 * np.pi * 5 * (t[:100]))  # Pattern to detect

# Perform cross-correlation using scipy's correlate
cross_corr = correlate(signal_1, signal_2, mode='full')

# Calculate lag values (index shift)
lags = np.arange(-len(signal_2) + 1, len(signal_1))

# Plot signals and cross-correlation
plt.figure(figsize=(10, 6))

# Plot the original signal and pattern
plt.subplot(2, 1, 1)
plt.plot(t, signal_1, label="Signal 1 (Noisy)")
plt.plot(t[:100], signal_2, label="Signal 2 (Pattern)", color='red')
plt.legend()
plt.title("Signal 1 and Signal 2")

# Plot the cross-correlation result
plt.subplot(2, 1, 2)
plt.plot(lags, cross_corr)
plt.title("Cross-Correlation between Signal 1 and Signal 2")
plt.xlabel("Lag")
plt.ylabel("Correlation Coefficient")

plt.tight_layout()
plt.show()
