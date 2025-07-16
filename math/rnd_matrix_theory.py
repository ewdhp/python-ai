"""
Random Matrix Theory Applications
This script demonstrates practical applications of random matrix theory in 
machine learning, statistics, and signal processing with detailed examples.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg
import seaborn as sns

print("=== RANDOM MATRIX THEORY APPLICATIONS ===")
print("Understanding eigenvalue distributions, spectral properties, and practical uses\n")

# Application 1: Marchenko-Pastur Law (Eigenvalue Distribution)
print("=== APPLICATION 1: MARCHENKO-PASTUR LAW ===")
print("Studies eigenvalue distribution of sample covariance matrices")

def marchenko_pastur_density(x, ratio, sigma=1):
    """Theoretical density of Marchenko-Pastur distribution"""
    if ratio > 1:
        return np.zeros_like(x)
    
    a = sigma**2 * (1 - np.sqrt(ratio))**2
    b = sigma**2 * (1 + np.sqrt(ratio))**2
    
    density = np.where(
        (x >= a) & (x <= b),
        np.sqrt((b - x) * (x - a)) / (2 * np.pi * sigma**2 * ratio * x),
        0
    )
    return density

# Generate random data matrix
n_samples, n_features = 1000, 500  # ratio = n_features/n_samples = 0.5
ratio = n_features / n_samples

np.random.seed(42)
X = np.random.randn(n_samples, n_features)

# Compute sample covariance matrix
C = (X.T @ X) / n_samples  # Sample covariance matrix

# Compute eigenvalues
eigenvalues = linalg.eigvals(C)
eigenvalues = eigenvalues.real  # Take real part

print(f"Matrix dimensions: {n_samples} × {n_features}")
print(f"Ratio (p/n): {ratio:.3f}")
print(f"Number of eigenvalues: {len(eigenvalues)}")
print(f"Largest eigenvalue: {np.max(eigenvalues):.3f}")
print(f"Smallest eigenvalue: {np.min(eigenvalues):.3f}")

# Plot histogram vs theoretical distribution
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.hist(eigenvalues, bins=50, density=True, alpha=0.7, color='skyblue', 
         label='Empirical eigenvalues')

# Theoretical Marchenko-Pastur density
x_theory = np.linspace(0, np.max(eigenvalues) * 1.1, 1000)
y_theory = marchenko_pastur_density(x_theory, ratio)
plt.plot(x_theory, y_theory, 'r-', linewidth=2, label='Marchenko-Pastur law')

plt.xlabel('Eigenvalue')
plt.ylabel('Density')
plt.title('Eigenvalue Distribution vs Theory')
plt.legend()
plt.grid(True, alpha=0.3)

# Application 2: Random Matrix Condition Numbers
print("\n=== APPLICATION 2: CONDITION NUMBER ANALYSIS ===")
print("Studying numerical stability through condition numbers")

def analyze_condition_numbers(sizes, n_trials=100):
    """Analyze condition numbers for different matrix sizes"""
    results = []
    
    for size in sizes:
        cond_numbers = []
        for _ in range(n_trials):
            # Generate random matrix
            A = np.random.randn(size, size)
            cond_num = np.linalg.cond(A)
            if not np.isinf(cond_num):  # Filter out infinite condition numbers
                cond_numbers.append(cond_num)
        
        results.append({
            'size': size,
            'mean_cond': np.mean(cond_numbers),
            'std_cond': np.std(cond_numbers),
            'median_cond': np.median(cond_numbers),
            'max_cond': np.max(cond_numbers)
        })
    
    return results

sizes = [10, 20, 50, 100, 200]
cond_results = analyze_condition_numbers(sizes)

print("Condition number statistics:")
print("Size\tMean\t\tMedian\t\tMax")
for result in cond_results:
    print(f"{result['size']}\t{result['mean_cond']:.2e}\t{result['median_cond']:.2e}\t{result['max_cond']:.2e}")

plt.subplot(1, 2, 2)
means = [r['mean_cond'] for r in cond_results]
stds = [r['std_cond'] for r in cond_results]
plt.errorbar(sizes, means, yerr=stds, marker='o', capsize=5)
plt.xlabel('Matrix Size')
plt.ylabel('Condition Number')
plt.title('Condition Numbers vs Matrix Size')
plt.yscale('log')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Application 3: Random Projections (Johnson-Lindenstrauss)
print("\n=== APPLICATION 3: JOHNSON-LINDENSTRAUSS EMBEDDINGS ===")
print("Dimensionality reduction preserving pairwise distances")

def johnson_lindenstrauss_bound(n_points, epsilon=0.1):
    """Compute the minimum embedding dimension"""
    return int(4 * np.log(n_points) / (epsilon**2 / 2 - epsilon**3 / 3))

def random_projection(X, target_dim, method='gaussian'):
    """Apply random projection to reduce dimensionality"""
    n_samples, n_features = X.shape
    
    if method == 'gaussian':
        # Gaussian random projection
        R = np.random.randn(n_features, target_dim) / np.sqrt(target_dim)
    elif method == 'sparse':
        # Sparse random projection (faster)
        R = np.random.choice([-1, 0, 1], size=(n_features, target_dim), 
                           p=[1/6, 2/3, 1/6]) / np.sqrt(target_dim)
    
    return X @ R

# Generate high-dimensional data
np.random.seed(123)
n_points = 100
original_dim = 1000
X_high = np.random.randn(n_points, original_dim)

# Compute optimal embedding dimension
epsilon = 0.1
min_dim = johnson_lindenstrauss_bound(n_points, epsilon)
print(f"Original dimension: {original_dim}")
print(f"Number of points: {n_points}")
print(f"Distortion tolerance (ε): {epsilon}")
print(f"Minimum embedding dimension: {min_dim}")

# Apply random projections
target_dims = [min_dim, 2*min_dim, 5*min_dim]
projections = {}

for dim in target_dims:
    projections[dim] = random_projection(X_high, dim)

# Compute pairwise distances
def compute_pairwise_distances(X):
    """Compute all pairwise distances"""
    n = X.shape[0]
    distances = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            dist = np.linalg.norm(X[i] - X[j])
            distances[i, j] = distances[j, i] = dist
    return distances

# Original distances
original_distances = compute_pairwise_distances(X_high)
orig_flat = original_distances[np.triu_indices_from(original_distances, k=1)]

print(f"\nDistance preservation analysis:")
print("Target Dim\tMean Error\tMax Error\t95% within ε")

plt.figure(figsize=(15, 5))

for i, dim in enumerate(target_dims):
    projected_distances = compute_pairwise_distances(projections[dim])
    proj_flat = projected_distances[np.triu_indices_from(projected_distances, k=1)]
    
    # Compute relative errors
    relative_errors = np.abs(proj_flat - orig_flat) / orig_flat
    mean_error = np.mean(relative_errors)
    max_error = np.max(relative_errors)
    within_epsilon = np.mean(relative_errors <= epsilon) * 100
    
    print(f"{dim}\t\t{mean_error:.4f}\t\t{max_error:.4f}\t\t{within_epsilon:.1f}%")
    
    # Plot distance comparison
    plt.subplot(1, 3, i+1)
    plt.scatter(orig_flat, proj_flat, alpha=0.5, s=1)
    plt.plot([0, np.max(orig_flat)], [0, np.max(orig_flat)], 'r--', alpha=0.7)
    
    # Error bounds
    x_line = np.linspace(0, np.max(orig_flat), 100)
    plt.fill_between(x_line, x_line*(1-epsilon), x_line*(1+epsilon), 
                    alpha=0.2, color='green', label=f'±{epsilon} error')
    
    plt.xlabel('Original Distance')
    plt.ylabel('Projected Distance')
    plt.title(f'Dim: {dim}\nMean Error: {mean_error:.3f}')
    plt.legend()

plt.tight_layout()
plt.show()

# Application 4: Spectral Clustering with Random Matrices
print("\n=== APPLICATION 4: SPECTRAL CLUSTERING ===")
print("Using random matrix theory for graph clustering")

def generate_stochastic_block_model(n_per_block=50, n_blocks=3, p_in=0.3, p_out=0.05):
    """Generate a stochastic block model graph"""
    n_total = n_per_block * n_blocks
    adj_matrix = np.zeros((n_total, n_total))
    
    # Generate block structure
    for i in range(n_total):
        for j in range(i+1, n_total):
            block_i = i // n_per_block
            block_j = j // n_per_block
            
            if block_i == block_j:
                prob = p_in  # Within block
            else:
                prob = p_out  # Between blocks
            
            if np.random.random() < prob:
                adj_matrix[i, j] = adj_matrix[j, i] = 1
    
    return adj_matrix

def spectral_clustering(adj_matrix, n_clusters):
    """Perform spectral clustering"""
    # Compute degree matrix
    degrees = np.sum(adj_matrix, axis=1)
    D = np.diag(degrees)
    
    # Compute normalized Laplacian
    D_sqrt_inv = np.diag(1.0 / np.sqrt(degrees + 1e-10))
    L_norm = np.eye(len(adj_matrix)) - D_sqrt_inv @ adj_matrix @ D_sqrt_inv
    
    # Compute eigenvalues and eigenvectors
    eigenvals, eigenvecs = linalg.eigh(L_norm)
    
    # Use smallest eigenvalues (Fiedler vectors)
    embedding = eigenvecs[:, :n_clusters]
    
    # K-means clustering in embedding space
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embedding)
    
    return labels, eigenvals, embedding

# Generate synthetic graph
np.random.seed(456)
n_blocks = 3
n_per_block = 30
adj_matrix = generate_stochastic_block_model(n_per_block, n_blocks)

print(f"Generated graph with {n_blocks} blocks of {n_per_block} nodes each")
print(f"Total nodes: {adj_matrix.shape[0]}")
print(f"Total edges: {np.sum(adj_matrix) // 2}")

# Apply spectral clustering
labels, eigenvals, embedding = spectral_clustering(adj_matrix, n_blocks)

# True labels for comparison
true_labels = np.repeat(range(n_blocks), n_per_block)

# Compute clustering accuracy
from sklearn.metrics import adjusted_rand_score
accuracy = adjusted_rand_score(true_labels, labels)
print(f"Clustering accuracy (ARI): {accuracy:.3f}")

# Visualize results
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.imshow(adj_matrix, cmap='Blues')
plt.title('Adjacency Matrix')
plt.colorbar()

plt.subplot(1, 3, 2)
plt.plot(eigenvals[:20], 'bo-')
plt.xlabel('Eigenvalue Index')
plt.ylabel('Eigenvalue')
plt.title('Laplacian Spectrum')
plt.grid(True, alpha=0.3)

plt.subplot(1, 3, 3)
colors = ['red', 'blue', 'green', 'orange', 'purple']
for i in range(n_blocks):
    mask = labels == i
    plt.scatter(embedding[mask, 0], embedding[mask, 1], 
               c=colors[i], label=f'Cluster {i}', alpha=0.7)
plt.xlabel('1st Eigenvector')
plt.ylabel('2nd Eigenvector')
plt.title('Spectral Embedding')
plt.legend()

plt.tight_layout()
plt.show()

# Application 5: Matrix Completion using Random Matrix Theory
print("\n=== APPLICATION 5: MATRIX COMPLETION ===")
print("Recovering missing entries using low-rank assumptions")

def generate_low_rank_matrix(m, n, rank, noise_level=0.1):
    """Generate a low-rank matrix with noise"""
    U = np.random.randn(m, rank)
    V = np.random.randn(rank, n)
    M = U @ V + noise_level * np.random.randn(m, n)
    return M, U, V

def random_mask(shape, observed_fraction=0.3):
    """Generate random observation mask"""
    mask = np.random.random(shape) < observed_fraction
    return mask

def nuclear_norm_minimization(M_observed, mask, max_iter=100, lr=0.01):
    """Simple nuclear norm minimization for matrix completion"""
    m, n = M_observed.shape
    M_completed = np.random.randn(m, n) * 0.1
    
    for iteration in range(max_iter):
        # SVD of current estimate
        U, s, Vt = linalg.svd(M_completed, full_matrices=False)
        
        # Soft thresholding (nuclear norm regularization)
        threshold = lr
        s_thresh = np.maximum(s - threshold, 0)
        
        # Reconstruct matrix
        M_new = U @ np.diag(s_thresh) @ Vt
        
        # Project onto observed entries
        M_completed = M_new.copy()
        M_completed[mask] = M_observed[mask]
        
        if iteration % 20 == 0:
            # Compute error on observed entries
            error = np.linalg.norm((M_completed - M_observed)[mask])
            print(f"Iteration {iteration}: Error = {error:.6f}, Rank ≈ {np.sum(s_thresh > 1e-3)}")
    
    return M_completed

# Generate test case
m, n, true_rank = 50, 40, 5
M_true, U_true, V_true = generate_low_rank_matrix(m, n, true_rank, noise_level=0.05)

# Create random observation mask
observed_fraction = 0.4
mask = random_mask((m, n), observed_fraction)
M_observed = M_true.copy()
M_observed[~mask] = 0  # Set unobserved entries to 0

print(f"Matrix size: {m} × {n}")
print(f"True rank: {true_rank}")
print(f"Observed entries: {np.sum(mask)} / {m*n} ({observed_fraction:.1%})")

# Apply matrix completion
M_completed = nuclear_norm_minimization(M_observed, mask)

# Compute recovery error
recovery_error = np.linalg.norm(M_completed - M_true, 'fro') / np.linalg.norm(M_true, 'fro')
print(f"Relative recovery error: {recovery_error:.4f}")

# Visualize results
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.imshow(M_true, cmap='RdBu', aspect='auto')
plt.title('True Matrix')
plt.colorbar()

plt.subplot(1, 3, 2)
M_observed_vis = M_observed.copy()
M_observed_vis[~mask] = np.nan
plt.imshow(M_observed_vis, cmap='RdBu', aspect='auto')
plt.title(f'Observed ({observed_fraction:.1%})')
plt.colorbar()

plt.subplot(1, 3, 3)
plt.imshow(M_completed, cmap='RdBu', aspect='auto')
plt.title(f'Completed (Error: {recovery_error:.3f})')
plt.colorbar()

plt.tight_layout()
plt.show()

print("\n=== RANDOM MATRIX THEORY SUMMARY ===")
print("""
KEY APPLICATIONS DEMONSTRATED:

1. MARCHENKO-PASTUR LAW:
   • Eigenvalue distribution of sample covariance matrices
   • Fundamental result connecting dimension ratio to spectrum
   • Applications: PCA, factor models, signal detection

2. CONDITION NUMBER ANALYSIS:
   • Numerical stability of linear systems
   • Growth with matrix size in random matrices
   • Applications: numerical linear algebra, optimization

3. JOHNSON-LINDENSTRAUSS EMBEDDINGS:
   • Dimensionality reduction with distance preservation
   • Theoretical guarantees for embedding dimension
   • Applications: nearest neighbor search, clustering

4. SPECTRAL CLUSTERING:
   • Graph clustering using eigenvalue decomposition
   • Random graph models and community detection
   • Applications: social networks, image segmentation

5. MATRIX COMPLETION:
   • Recovering missing entries from partial observations
   • Low-rank assumptions and nuclear norm minimization
   • Applications: recommender systems, image inpainting

THEORETICAL FOUNDATIONS:
• Wigner's semicircle law for symmetric random matrices
• Tracy-Widom distribution for largest eigenvalues
• Concentration of measure phenomena
• Free probability theory connections

PRACTICAL IMPACT:
• Machine learning: PCA, clustering, dimensionality reduction
• Signal processing: array processing, source separation
• Statistics: high-dimensional inference, covariance estimation
• Data science: matrix completion, network analysis
""")
