import matplotlib
matplotlib.use('TkAgg')  # Use the 'TkAgg' backend for interactive plotting

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def visualize_3d_linked_list(linked_list):
    try:
        print("Starting visualization...")

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Extract nodes for visualization
        nodes = []
        node = linked_list.head
        while node:
            nodes.append(node.value)
            node = node.next
            if node == linked_list.head:
                break

        if not nodes:
            print("No nodes found in the linked list.")
            return

        print(f"Nodes extracted: {nodes}")

        # Plot nodes
        xs, ys, zs = zip(*nodes)
        ax.scatter(xs, ys, zs, c='r', marker='o')

        # Create a mesh for visualization
        vertices = [list(nodes)]
        ax.add_collection3d(Poly3DCollection(vertices, alpha=.25, linewidths=1, edgecolors='r'))

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.show()  # Display the plot

        print("Visualization completed and displayed.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            self.head.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head

def generate_sphere_points(radius, num_points):
    points = []
    for _ in range(num_points):
        theta = np.random.uniform(0, 2 * np.pi)
        phi = np.random.uniform(0, np.pi)
        x = radius * np.sin(phi) * np.cos(theta)
        y = radius * np.sin(phi) * np.sin(theta)
        z = radius * np.cos(phi)
        points.append((x, y, z))
    return points

# Create a circular linked list and visualize it
linked_list = CircularLinkedList()
sphere_points = generate_sphere_points(radius=1, num_points=100)
for point in sphere_points:
    linked_list.append(point)

visualize_3d_linked_list(linked_list)