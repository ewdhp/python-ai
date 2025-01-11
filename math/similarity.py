import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn.metrics.pairwise import cosine_similarity

# Generate random variables
np.random.seed(42)
x = np.random.normal(0, 1, 1000)
y = 2 * x + np.random.normal(0, 1, 1000)  # Correlated with x
z = np.random.normal(0, 1, 1000)  # Independent of x

# Calculate Pearson correlation coefficient
correlation_xy, _ = pearsonr(x, y)
correlation_xz, _ = pearsonr(x, z)

# Calculate cosine similarity
cosine_sim_xy = cosine_similarity(x.reshape(1, -1), y.reshape(1, -1))[0, 0]
cosine_sim_xz = cosine_similarity(x.reshape(1, -1), z.reshape(1, -1))[0, 0]

# Plot the random variables
plt.figure(figsize=(18, 6))

# Scatter plot for correlation
plt.subplot(1, 3, 1)
plt.scatter(x, y, alpha=0.5, label=f'Correlation: {correlation_xy:.2f}')
plt.scatter(x, z, alpha=0.5, label=f'Correlation: {correlation_xz:.2f}')
plt.xlabel('X')
plt.ylabel('Y and Z')
plt.title('Correlation')
plt.legend()

# Histogram for statistical independence
plt.subplot(1, 3, 2)
plt.hist(x, bins=30, alpha=0.5, label='X')
plt.hist(z, bins=30, alpha=0.5, label='Z')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Statistical Independence')
plt.legend()

# Bar plot for cosine similarity
plt.subplot(1, 3, 3)
plt.bar(['X-Y', 'X-Z'], [cosine_sim_xy, cosine_sim_xz], color=['blue', 'orange'])
plt.xlabel('Variable Pairs')
plt.ylabel('Cosine Similarity')
plt.title('Cosine Similarity')

plt.tight_layout()
plt.show()