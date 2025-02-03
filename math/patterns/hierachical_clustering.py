import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

# Example data points (2D coordinates)
data = np.array([
    [1, 2],
    [2, 3],
    [3, 4],
    [8, 9],
    [8, 10],
    [25, 30]
])

# Perform hierarchical/agglomerative clustering
Z = linkage(data, method='ward')

# Create a dendrogram to visualize the clustering
plt.figure(figsize=(10, 6))
dendrogram(Z)
plt.title("Hierarchical Clustering Dendrogram")
plt.xlabel("Sample index")
plt.ylabel("Distance")
plt.show()
