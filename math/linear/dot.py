import numpy as np

import matplotlib.pyplot as plt

# Define two vectors
a = np.array([2, 3])
b = np.array([4, 1])



# 1. Sum of Products (Algebraic Definition)
print("\n1. Sum of Products (Algebraic Definition):")
print(f"{'aᵢ':>3} {'bᵢ':>3} {'aᵢ × bᵢ':>8}")
print("-" * 18)
for ai, bi in zip(a, b):
    print(f"{ai:>3} {bi:>3} {ai*bi:>8}")
print("-" * 18)
print(f"{'':>3} {'':>3} {np.dot(a, b):>8}")
print(f"Dot product: {np.dot(a, b)}")

# 2. Geometric Interpretation
print("\n2. Geometric Interpretation:")
norm_a = np.linalg.norm(a)
norm_b = np.linalg.norm(b)
cos_theta = np.dot(a, b) / (norm_a * norm_b)
theta_rad = np.arccos(np.clip(cos_theta, -1.0, 1.0))
theta_deg = np.degrees(theta_rad)
print(f"|a| = {norm_a:.3f}, |b| = {norm_b:.3f}")
print(f"cos(θ) = {cos_theta:.3f}, θ = {theta_deg:.2f}°")
print(f"Dot = |a| × |b| × cos(θ) = {norm_a:.3f} × {norm_b:.3f} × {cos_theta:.3f} = {norm_a*norm_b*cos_theta:.3f}")

# 3. Projection
print("\n3. Projection of a onto b:")
b_unit = b / norm_b
proj_length = np.dot(a, b_unit)
proj = proj_length * b_unit
print(f"Unit vector of b: {b_unit}")
print(f"Projection length: {proj_length:.3f}")
print(f"Projection vector: {proj}")

# 4. Matrix Multiplication
print("\n4. Matrix Multiplication:")
a_row = a.reshape(1, -1)
b_col = b.reshape(-1, 1)
print(f"a as row: {a_row}")
print(f"b as column: {b_col}")
print(f"a @ b_col = {a_row @ b_col} (scalar)")

# 5. Orthogonality
print("\n5. Orthogonality:")
if np.isclose(np.dot(a, b), 0):
    print("Vectors are orthogonal (perpendicular).")
else:
    print("Vectors are not orthogonal (dot ≠ 0).")

# 6. Work in Physics
print("\n6. Work in Physics:")
print("If a force vector F moves an object along displacement d, work = F · d.")
print(f"Here, F = {a}, d = {b}, so work = {np.dot(a, b)}")

# 7. Cosine Similarity
print("\n7. Cosine Similarity:")
print(f"cosine_similarity = dot(a, b) / (|a| * |b|) = {cos_theta:.3f}")
print(f"This is the cosine of the angle between the vectors, a measure of their directional similarity.")

# Plot the vectors
plt.figure(figsize=(6,6))
plt.quiver(0, 0, a[0], a[1], angles='xy', scale_units='xy', scale=1, color='r', label='a')
plt.quiver(0, 0, b[0], b[1], angles='xy', scale_units='xy', scale=1, color='b', label='b')

# Draw projection of a onto b
b_unit = b / np.linalg.norm(b)
proj_length = np.dot(a, b_unit)
proj = proj_length * b_unit
plt.quiver(0, 0, proj[0], proj[1], angles='xy', scale_units='xy', scale=1, color='g', label='Projection of a onto b')
plt.scatter([proj[0]], [proj[1]], color='g', marker='o')

plt.xlim(-1, 6)
plt.ylim(-1, 6)
plt.grid()
plt.legend()
plt.title("Dot Product Visualization")
plt.xlabel("X")
plt.ylabel("Y")
plt.gca().set_aspect('equal', adjustable='box')
plt.show()