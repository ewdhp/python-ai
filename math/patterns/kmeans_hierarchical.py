import numpy as np

# Function to calculate Euclidean distance
def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

# K-Means algorithm implementation with detailed logs
def kmeans(X, k, max_iters=100):
    # Randomly initialize centroids
    centroids = X[np.random.choice(X.shape[0], k, replace=False)]
    prev_centroids = np.zeros_like(centroids)
    labels = np.zeros(X.shape[0])

    print("Initial centroids:\n", centroids)
    
    for iteration in range(max_iters):
        print(f"\nIteration {iteration + 1}:")
        
        # Assign each point to the nearest centroid
        for i in range(X.shape[0]):
            distances = np.array([euclidean_distance(X[i], c) for c in centroids])
            labels[i] = np.argmin(distances)
        
        print(f"Labels: {labels}")
        
        # Store current centroids to check for convergence
        prev_centroids = centroids.copy()

        # Update centroids by taking the mean of points in each cluster
        for j in range(k):
            centroids[j] = np.mean(X[labels == j], axis=0)

        print(f"Updated centroids: {centroids}")

        # Check for convergence (if centroids do not change)
        if np.all(centroids == prev_centroids):
            print("Convergence reached!")
            break

    return labels, centroids

# Example usage
data = np.array([
    [1, 2],
    [1, 3],
    [2, 2],
    [8, 8],
    [8, 9],
    [9, 8]
])

# Running K-Means clustering with 2 clusters
labels, centroids = kmeans(data, k=2)
print("\nFinal Cluster Labels: ", labels)
print("Final Centroids: ", centroids)
