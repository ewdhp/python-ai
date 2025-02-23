import numpy as np
import matplotlib.pyplot as plt

# Generate values for x between pi/2 and 3*pi/2 (avoiding the discontinuity at pi/2 and 3*pi/2)
x = np.linspace(np.pi/2 + 0.01, 3*np.pi/2 - 0.01, 1000)

# Calculate the tangent values for y
y = np.tan(x)

# Set up the figure and subplots
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Plot the tangent function on the first subplot
axs[0].plot(x, y, label=r'$\tan(x)$')
axs[0].axhline(0, color='black',linewidth=1)
axs[0].axvline(np.pi/2, color='red', linestyle='--', label=r'$\frac{\pi}{2}$')
axs[0].axvline(3*np.pi/2, color='red', linestyle='--', label=r'$\frac{3\pi}{2}$')
axs[0].set_title('Plot of Tangent Function from pi/2 to 3pi/2')
axs[0].set_xlabel('x')
axs[0].set_ylabel('tan(x)')
axs[0].legend()
axs[0].grid(True)

# Create a unit circle in the second subplot
theta = np.linspace(0, 2*np.pi, 100)
x_circle = np.cos(theta)
y_circle = np.sin(theta)
axs[1].plot(x_circle, y_circle, label='Unit Circle', color='b')

# Mark common values of pi between pi/2 and 3pi/2 on the unit circle (pi, 2pi)
pi_values = [np.pi]  # Only mark pi within the range
for pi_value in pi_values:
    x_mark = np.cos(pi_value)
    y_mark = np.sin(pi_value)
    axs[1].plot(x_mark, y_mark, 'ro')  # Red marker for pi multiples
    axs[1].text(x_mark * 1.1, y_mark * 1.1, f'${pi_value/np.pi:.0f}\\pi$', fontsize=12, color='red')

# Mark 3pi/2 explicitly for clarity, as it's the end point in the range
x_mark_3pi2 = np.cos(3*np.pi/2)
y_mark_3pi2 = np.sin(3*np.pi/2)
axs[1].plot(x_mark_3pi2, y_mark_3pi2, 'go')  # Green marker for 3*pi/2
axs[1].text(x_mark_3pi2 * 1.1, y_mark_3pi2 * 1.1, r'$\frac{3\pi}{2}$', fontsize=12, color='green')

# Set title and labels for the unit circle plot
axs[1].set_title('Unit Circle with Common Pi Values Between pi/2 and 3pi/2')
axs[1].set_xlabel('x')
axs[1].set_ylabel('y')
axs[1].axis('equal')
axs[1].grid(True)
axs[1].legend()

# Show the plots
plt.tight_layout()
plt.show()
