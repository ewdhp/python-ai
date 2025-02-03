import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Generate two signals: one with a linear relationship and another with noise
np.random.seed(0)

# Signal 1: A linearly increasing signal
x = np.linspace(0, 10, 100)
signal_1 = 2 * x + 1  # Linear relationship

# Signal 2: A noisy version of signal_1 with some random noise added
signal_2 = signal_1 + np.random.normal(0, 1, 100)  # Adding noise

# Compute the correlation coefficient (Pearson correlation)
correlation, _ = pearsonr(signal_1, signal_2)

# Plot the signals and the correlation coefficient
plt.figure(figsize=(10, 6))

# Plot both signals
plt.plot(x, signal_1, label="Signal 1 (Linear)", linewidth=2)
plt.plot(x, signal_2, label="Signal 2 (Noisy)", linewidth=2)
plt.legend()

# Title and labels
plt.title(f"Signals with Correlation Coefficient: {correlation:.2f}")
plt.xlabel("X")
plt.ylabel("Signal Value")

plt.tight_layout()
plt.show()

# Print the correlation coefficient
print(f"Correlation Coefficient: {correlation:.2f}")
