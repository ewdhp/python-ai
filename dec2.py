#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# --- Quantum Setup ---

theta = np.pi / 6  # 30 degrees
v_theta = np.array([np.cos(theta), np.sin(theta)])
scale = 1e6
r_A_inf = scale * v_theta
half_factor = 1 / np.sqrt(2)
r_B_half = half_factor * r_A_inf
ROC_radius = 1.0
z_B = ROC_radius * np.exp(1j * theta)

# Circle of possible B positions (before decoherence)
theta_vals = np.linspace(0, 2 * np.pi, 300)
circle_points = np.array([[np.cos(t), np.sin(t)] for t in theta_vals])
quantum_circle = half_factor * circle_points  # superposition before collapse

# Simulate decoherence: remove part of the arc (simulate partial collapse)
decoherence_start = np.pi / 4
decoherence_end = 3 * np.pi / 4
mask = (theta_vals >= decoherence_start) & (theta_vals <= decoherence_end)
decohered_arc = half_factor * np.array([[np.cos(t), np.sin(t)] for t in theta_vals[mask]])

# --- Plotting ---

fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# === Plot 1: Real-space with decoherence and collapse ===
ax[0].set_title("Real Space: Superposition → Decoherence → Collapse")
ax[0].set_xlim(0, 1.2)
ax[0].set_ylim(0, 1.2)
ax[0].set_aspect('equal')
ax[0].grid(True)

# Unit square
ax[0].plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], 'k--', alpha=0.3)

# Full quantum circle (possible B states pre-decoherence)
ax[0].plot(quantum_circle[:, 0], quantum_circle[:, 1], color='purple', linestyle='--', alpha=0.4, label='Quantum Superposition (B)')

# Decohered region
ax[0].plot(decohered_arc[:, 0], decohered_arc[:, 1], color='orange', linewidth=3, label='Decohered Zone')

# Collapse: Estimated B after decoherence
ax[0].plot(r_B_half[0] / scale, r_B_half[1] / scale, 'go', label='Collapsed B (1/√2 midpoint)')

# Vector from origin to B
ax[0].quiver(0, 0, r_B_half[0] / scale, r_B_half[1] / scale, angles='xy', scale_units='xy', scale=1, color='green', alpha=0.7)

# Vector to A
ax[0].quiver(0, 0, v_theta[0], v_theta[1], angles='xy', scale_units='xy', scale=1, color='gray', alpha=0.5, label="Direction to A (→∞)")

ax[0].legend()

# === Plot 2: Z-Plane View ===
ax[1].set_title("Z-Plane: ROC and Collapse to Edge")
ax[1].set_xlim(-1.2, 1.2)
ax[1].set_ylim(-1.2, 1.2)
ax[1].set_aspect('equal')
ax[1].grid(True)

# ROC circle
roc_circle = plt.Circle((0, 0), ROC_radius, color='gray', fill=False, linestyle='--', label='ROC Boundary')
ax[1].add_artist(roc_circle)

# Full superposition on ROC
ax[1].plot(ROC_radius * np.cos(theta_vals), ROC_radius * np.sin(theta_vals), color='purple', linestyle='--', alpha=0.3)

# Decohered arc
arc_complex = ROC_radius * np.exp(1j * theta_vals[mask])
ax[1].plot(np.real(arc_complex), np.imag(arc_complex), color='orange', linewidth=3, label='Decohered Arc (Z-plane)')

# Collapsed state on ROC
ax[1].plot(np.real(z_B), np.imag(z_B), 'bo', label="Collapsed B (on ROC edge)")

# Vector from origin to collapsed B
ax[1].arrow(0, 0, np.real(z_B), np.imag(z_B), head_width=0.05, color='blue', alpha=0.7)

# Origin
ax[1].plot(0, 0, 'ko')

ax[1].legend()

plt.tight_layout()
plt.show()
