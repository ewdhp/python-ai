import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

# Example adjacency matrix (relationship data)
adj_matrix = np.array([
    [1, 1, 0, 0, 1],
    [1, 1, 1, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 1, 1],
    [1, 0, 0, 1, 1]
])

# Calculate cosine similarity between rows (people)
similarity_matrix = cosine_similarity(adj_matrix)

# Apply K-Means clustering (assuming K=2)
kmeans = KMeans(n_clusters=2)
kmeans.fit(similarity_matrix)

# Print cluster labels
print("Cluster Labels: ", kmeans.labels_)

# Output the centroids (mean relationship vectors)
print("Centroids: ", kmeans.cluster_centers_)
