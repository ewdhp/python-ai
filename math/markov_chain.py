import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns

# Define transition matrices for two Markov Chains
P1 = np.array([[0.1, 0.6, 0.3],
               [0.4, 0.4, 0.2],
               [0.2, 0.3, 0.5]])

P2 = np.array([[0.2, 0.5, 0.3],
               [0.3, 0.4, 0.3],
               [0.3, 0.3, 0.4]])

# Flatten the transition matrices to vectors
P1_flat = P1.flatten().reshape(1, -1)
P2_flat = P2.flatten().reshape(1, -1)

# Calculate cosine similarity between the two Markov Chains
cosine_sim = cosine_similarity(P1_flat, P2_flat)[0, 0]

# Display the cosine similarity
print(f"Cosine similarity between the two Markov Chains: {cosine_sim:.2f}")

# Visual representation of the transition matrices
plt.figure(figsize=(12, 6))

# Heatmap for the first Markov Chain
plt.subplot(1, 2, 1)
sns.heatmap(P1, annot=True, cmap='Blues', cbar=False)
plt.title('Transition Matrix of Markov Chain 1')
plt.xlabel('State')
plt.ylabel('State')

# Heatmap for the second Markov Chain
plt.subplot(1, 2, 2)
sns.heatmap(P2, annot=True, cmap='Blues', cbar=False)
plt.title('Transition Matrix of Markov Chain 2')
plt.xlabel('State')
plt.ylabel('State')

plt.tight_layout()
plt.show()