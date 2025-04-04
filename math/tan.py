import numpy as np
import matplotlib.pyplot as plt

# Generate x values
x = np.linspace(0, 2 * np.pi, 100)

# Compute sine and cosine values
sin_y = np.tan(x) * np.sin(x)
cos_y = np.tan(x + np.pi * 2) * np.sin(x + np.pi / 2)

# Create the figure
fig = plt.figure(figsize=(8, 10))

# Create rectilinear subplot for sine function
ax1 = fig.add_subplot(2, 1, 1, projection='rectilinear')
ax1.plot(x, sin_y, label='sin(x)', color='b')
ax1.set_xlabel('x')
ax1.set_ylabel('sin(x)')
ax1.set_title('Sine Function')
ax1.legend()

# Create polar subplot for cosine function and sin function
ax2 = fig.add_subplot(2, 1, 2, projection='polar')
ax2.plot(x, cos_y, label='cos(x)', color='r')
ax2.plot(x, sin_y, label='sin(x)', color='b')
ax2.set_title('Cosine Function')
ax2.legend()


# Adjust layout and display the plot
plt.tight_layout()
plt.show()