import numpy as np
import matplotlib.pyplot as plt

# --- Updated Model Settings ---

# Particle A going to infinity — simulate with large values in direction of deflection
# Choose direction vector first (say, fixed theta for illustration)
theta = np.pi / 6  # 30 degrees
v_theta = np.array([np.cos(theta), np.sin(theta)])

# Simulate Particle A at "infinity" in direction of v_theta (scaled large)
scale = 1e6
r_A_inf = scale * v_theta

# Use 1/sqrt(2) as the "half" weight factor
half_factor = 1 / np.sqrt(2)

# --- Midpoint-style estimate for Particle B using this new definition ---
# B lies between origin and "infinite" particle A direction, weighted by half_factor
r_B_half = half_factor * r_A_inf

# Also compute complex version at ROC edge
ROC_radius = 1.0
z_B = ROC_radius * np.exp(1j * theta)

# --- Plotting ---

fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# --- Plot 1: Real-space estimate with Particle A at infinity ---
ax[0].set_title("Real Space: Particle A → ∞, Midpoint Estimate for B")
ax[0].set_xlim(0, 1.2)
ax[0].set_ylim(0, 1.2)
ax[0].set_aspect('equal')
ax[0].grid(True)

# Draw vector from origin to A (scaled down for plotting)
ax[0].quiver(0, 0, v_theta[0], v_theta[1], angles='xy', scale_units='xy', scale=1, color='gray', alpha=0.5, label="Direction to A (→∞)")

# Plot estimated B from midpoint definition using 1/sqrt(2)
ax[0].plot(r_B_half[0] / scale, r_B_half[1] / scale, 'go', label="Particle B (1/√2 midpoint)")

# Draw vector to B
ax[0].quiver(0, 0, r_B_half[0] / scale, r_B_half[1] / scale, angles='xy', scale_units='xy', scale=1, color='green', alpha=0.7)

ax[0].legend()

# --- Plot 2: Complex Z-plane view ---
ax[1].set_title("Z-Plane: ROC and Particle B on Edge (Angle from A)")
ax[1].set_xlim(-1.2, 1.2)
ax[1].set_ylim(-1.2, 1.2)
ax[1].set_aspect('equal')
ax[1].grid(True)

# Draw ROC circle
roc_circle = plt.Circle((0, 0), ROC_radius, color='gray', fill=False, linestyle='--', label='ROC Boundary')
ax[1].add_artist(roc_circle)

# Plot B at edge of ROC
ax[1].plot(np.real(z_B), np.imag(z_B), 'bo', label="Particle B (on ROC edge)")

# Draw vector
ax[1].arrow(0, 0, np.real(z_B), np.imag(z_B), head_width=0.05, color='blue', alpha=0.7)

# Origin
ax[1].plot(0, 0, 'ko')

ax[1].legend()

plt.tight_layout()
plt.show()
