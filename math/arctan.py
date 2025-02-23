import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# Setup the figure and axes for both plots (time and magnitude responses)
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Angle values from 0 to 360 degrees (time domain)
theta_vals = np.linspace(0, 2 * np.pi, 200)  # Radians

# Unit Circle Setup (Left Plot: Time Response)
ax[0].set_xlim(-1.2, 1.2)
ax[0].set_ylim(-1.2, 1.2)
ax[0].set_aspect('equal')
ax[0].set_title("Unit Circle (Time Response)")

# Plot unit circle
circle = plt.Circle((0, 0), 1, color='blue', fill=False)
ax[0].add_patch(circle)

# Moving point on the unit circle
point_circle, = ax[0].plot([], [], 'ro', markersize=6)

# Sine line (vertical component)
sine_line, = ax[0].plot([], [], 'g-', lw=1)

# Tangent line (from the unit circle point)
tangent_line, = ax[0].plot([], [], 'r-', lw=1)

# Time-Domain Sine Plot (Right Plot: Magnitude Response)
time_vals = np.linspace(0, 2 * np.pi, 200)  # Time-domain angle values (radians)
sine_vals = np.sin(time_vals)  # Sine function values

ax[1].set_xlim(0, 2 * np.pi)
ax[1].set_ylim(-1.5, 1.5)
ax[1].plot(time_vals, sine_vals, 'b', label=r'$y = \sin(\theta)$')  # Sine curve
ax[1].set_title("Sine Function (Time Domain)")
ax[1].set_xlabel("Angle (radians)")
ax[1].set_ylabel("sin(x)")
ax[1].legend()

# Moving point on sine curve
point_sine, = ax[1].plot([], [], 'ro', markersize=6)

# Animation function to update both plots
def update(frame):
    theta = theta_vals[frame]  # Current angle in radians
    x = np.cos(theta)
    y = np.sin(theta)
    
    # Update unit circle point
    point_circle.set_data([x], [y])

    # Update sine line (vertical component of the unit circle point)
    sine_line.set_data([0, 0], [0, y])

    # Update tangent line (if within limits)
    if np.abs(np.cos(theta)) > 1e-2:  # Avoid division by zero
        tan_x = 1 / np.cos(theta)
        tangent_line.set_data([x, tan_x], [y, np.tan(theta)])
    else:
        tangent_line.set_data([], [])  # Hide tangent line at vertical asymptotes

    # Update sine function plot (time-domain response)
    point_sine.set_data([theta], [y])

    return point_circle, sine_line, tangent_line, point_sine

# Create animation
ani = animation.FuncAnimation(fig, update, frames=len(theta_vals), interval=50, blit=True)

# Show the plot
plt.tight_layout()
plt.show()
