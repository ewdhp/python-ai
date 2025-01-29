import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine, euclidean
from fastdtw import fastdtw  # Install with 'pip install fastdtw'


# Original signal (size 100)
signal = np.random.randint(0, 9, 100)

# New signal (size 10)
new_signal = [2, 6, 0, 7, 1, 3, 5, 8, 4, 6]

# Combine the two signals
signal = np.concatenate((signal, new_signal))

pattern = np.array([1, 2])  # Pattern to detect
window_size = len(pattern)

# Threshold for match detection
threshold = 0.50  # Can be adjusted

# Debug: Print the generated signal
print(f"Signal with key-value pairs:")
for idx, val in enumerate(signal):
    print(f"Index {idx}: {val}")

# Step 1: Apply KMeans clustering
kmeans = KMeans(n_clusters=3)
signal_reshaped = signal.reshape(-1, 1)  # Reshape for KMeans
kmeans.fit(signal_reshaped)
labels = kmeans.predict(signal_reshaped)

# Cluster Summary
cluster_summary = {}
for label in np.unique(labels):
    cluster_points = signal[labels == label]
    cluster_summary[label] = {
        "count": len(cluster_points),
        "range": (min(cluster_points), max(cluster_points))
    }

print("\nCluster Summary:")
for label, summary in cluster_summary.items():
    print(f"Cluster {label}: {summary['count']} points, Value Range: {summary['range']}")

# Step 2: Detect anomalies within each cluster using Isolation Forest
iso_forest = IsolationForest(contamination=0.1)  # 10% contamination for anomalies
anomalies = iso_forest.fit_predict(signal_reshaped)

# Anomaly Summary
anomalies_indices = [i for i, a in enumerate(anomalies) if a == -1]
print(f"\nAnomaly Summary:")
print(f"Total anomalies: {len(anomalies_indices)}")
print(f"Anomaly indices: {anomalies_indices}")
print(f"Anomalous values: {[signal[i] for i in anomalies_indices]}")

# Function for detecting patterns using different similarity metrics
def detect_pattern(signal, pattern, threshold, similarity_metric):
    matches = []
    for i in range(len(signal) - window_size + 1):
        window = signal[i:i + window_size]
        
        # Skip anomalies
        if anomalies[i] == -1:
            continue
        
        # Calculate similarity based on chosen metric
        if similarity_metric == 'cosine':
            similarity = 1 - cosine(window, pattern)
        elif similarity_metric == 'euclidean':
            similarity = 1 / (1 + euclidean(window, pattern))  # Inverse of distance to get similarity
        elif similarity_metric == 'dtw':
            distance, _ = fastdtw(window, pattern)
            similarity = 1 / (1 + distance)  # Inverse of distance to get similarity
        else:
            raise ValueError(f"Unknown similarity metric: {similarity_metric}")
        
        # Compare similarity to threshold
        if similarity > threshold:
            matches.append((i, labels[i], similarity))  # Record index, cluster label, and similarity
    
    return matches

# Detect patterns using different metrics
metrics = ['cosine', 'euclidean', 'dtw']
for metric in metrics:
    matches = detect_pattern(signal, pattern, threshold, metric)
    
    # Output results for each metric
    print(f"\nPattern detected using {metric} similarity at positions (with cluster labels): {matches}")

    # Optionally, you can display similarity scores as well for further analysis
    if matches:
        print(f"Summary of matches for {metric}:")
        for match in matches:
            print(f"Position {match[0]}, Cluster {match[1]}, Similarity: {match[2]:.2f}")
