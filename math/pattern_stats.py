import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine, euclidean
from fastdtw import fastdtw  # Install with 'pip install fastdtw'

# Example data
signal = [1.00, 1.3456789, 3.4567890]
pattern = [2, 1.3456789, 2.4567889]

# Convert signal to a NumPy array
signal = np.array(signal)  # Keep it as a 1D array
pattern = np.array(pattern)  # Ensure pattern is also 1D

window_size = len(pattern)

# Threshold for match detection
threshold = 0.90 # Can be adjusted

# Function for detecting patterns using different similarity metrics (set-based matching)
def detect_pattern(signal, pattern, threshold, similarity_metric):
    matches = []
    pattern_set = set(pattern)  # Convert the pattern to a set for flexible matching
    
    for i in range(len(signal) - window_size + 1):
        window = signal[i:i + window_size]
        
        # Skip anomalies (if you implement anomaly detection, this would be relevant)
        # if anomalies[i] == -1:
        #     continue
        
        window_set = set(window)  # Convert the window to a set for flexible matching
        
        # Calculate similarity based on set intersection
        if similarity_metric == 'set':
            intersection = len(pattern_set.intersection(window_set))  # Count the number of matching elements
            similarity = intersection / len(pattern_set)  # Normalize by the length of the pattern set
        elif similarity_metric == 'cosine':
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
            matches.append((i, similarity))  # Record index and similarity
    
    return matches

# Detect patterns using set-based similarity (order doesn't matter)
metrics = ['set', 'cosine', 'euclidean', 'dtw']
for metric in metrics:
    matches = detect_pattern(signal, pattern, threshold, metric)
    
    # Output results for each metric
    print(f"\nPattern detected using {metric} similarity at positions:\n")
    
    # Formatting the output as a matrix-like table
    if matches:
        print(f"{'Position':<10}{'Similarity':<15}")
        print("-" * 25)
        for match in matches:
            print(f"{match[0]:<10}{match[1]:<15.2f}")
        print("\n")
    else:
        print(f"No matches found using {metric} similarity.\n")
