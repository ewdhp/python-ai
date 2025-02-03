import math
import matplotlib.pyplot as plt

def circle_points(radius, num_points):
    points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append((x, y))
    return points

# Example usage
radius = 1
num_points = 8
points = circle_points(radius, num_points)

# Plotting the points
plt.figure(figsize=(6, 6))
plt.gca().set_aspect('equal', adjustable='box')
circle = plt.Circle((0, 0), radius, color='blue', fill=False)
plt.gca().add_artist(circle)

for i, (x, y) in enumerate(points):
    plt.plot(x, y, 'ro')  # Plot the point
    plt.text(x, y, f'P{i+1}', fontsize=12, ha='right')  # Add the tag

plt.xlim(-radius-0.5, radius+0.5)
plt.ylim(-radius-0.5, radius+0.5)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Key Points on the Circle')
plt.grid(True)
plt.show()