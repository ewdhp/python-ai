import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def cross_product_and_visualize(A, B):
    # Ensure 3D vectors
    if len(A) != 3 or len(B) != 3:
        raise ValueError("Both vectors must be 3-dimensional.")

    a1, a2, a3 = A
    b1, b2, b3 = B

    # Explicit cross product
    cross_product = (
        a2 * b3 - a3 * b2,
        a3 * b1 - a1 * b3,
        a1 * b2 - a2 * b1
    )
    area = np.linalg.norm(cross_product)

    # Convert to numpy arrays for plotting
    A = np.array(A)
    B = np.array(B)
    C = np.array(cross_product)

    # Set up 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    origin = np.array([0, 0, 0])

    # Draw vectors
    ax.quiver(*origin, *A, color='blue', label='Vector A')
    ax.quiver(*origin, *B, color='green', label='Vector B')
    ax.quiver(*origin, *C, color='red', label='Cross Product (A × B)')

    # Draw parallelogram span by A and B
    ax.plot_trisurf(
        [0, A[0], B[0], A[0] + B[0]],
        [0, A[1], B[1], A[1] + B[1]],
        [0, A[2], B[2], A[2] + B[2]],
        color='lightgrey',
        alpha=0.5
    )

    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-10, 10])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f"Cross Product Visualization\nArea = {area:.2f}")
    ax.legend()
    plt.show()

# Example usage
A = [1, 2, 3]
B = [4, 5, 6]
cross_product_and_visualize(A, B)