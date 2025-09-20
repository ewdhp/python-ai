import numpy as np
import matplotlib.pyplot as plt

# --- Basic Setup ---

ROC_radius_main = 1.0
ROC_radius_small = ROC_radius_main / 2  # Half the main ROC radius
theta_vals = np.linspace(0, 2 * np.pi, 400)

# Decoherence zone on main ROC (original)
theta_deco_start = np.pi / 4  # 45°
theta_deco_end = 3 * np.pi / 4  # 135°
mask_deco = (theta_vals >= theta_deco_start) & (theta_vals <= theta_deco_end)
arc_decoherence = ROC_radius_main * np.exp(1j * theta_vals[mask_deco])

# Opposite arc on main ROC (reflected / preserved coherence)
theta_opp_start = (theta_deco_start + np.pi) % (2 * np.pi)
theta_opp_end = (theta_deco_end + np.pi) % (2 * np.pi)
theta_vals_wrapped = theta_vals % (2 * np.pi)

# Handle wrap-around for opposite arc mask
if theta_opp_start < theta_opp_end:
    mask_opp = (theta_vals_wrapped >= theta_opp_start) & (theta_vals_wrapped <= theta_opp_end)
else:
    mask_opp = (theta_vals_wrapped >= theta_opp_start) | (theta_vals_wrapped <= theta_opp_end)
arc_opposite = ROC_radius_main * np.exp(1j * theta_vals[mask_opp])

# Tangent point (max derivative) — midpoint of decoherence arc on main ROC
theta_tangent = (theta_deco_start + theta_deco_end) / 2
point_tangent = ROC_radius_main * np.exp(1j * theta_tangent)
tangent_vec = 0.3 * 1j * np.exp(1j * theta_tangent)  # orthogonal vector to arc (tangent)

# Toy entangled state represented: |ψ⟩ = 1/√2 (|A0⟩|B1⟩ + |A1⟩|B0⟩)
# We will place A on decohered arc, B on opposite

theta_A = theta_tangent  # place A at center of decoherence
theta_B = (theta_A + np.pi) % (2 * np.pi)  # B in opposite arc
pos_A = ROC_radius_main * np.exp(1j * theta_A)
pos_B = ROC_radius_main * np.exp(1j * theta_B)

# --- New smaller ROC, shifted by pi/4 radians ---

theta_shift = np.pi / 4
theta_vals_shifted = (theta_vals + theta_shift) % (2 * np.pi)
roc_small_circle = ROC_radius_small * np.exp(1j * theta_vals_shifted)

# --- Plotting ---
fig, ax = plt.subplots(figsize=(9, 9))
ax.set_title("Main ROC + Smaller Shifted ROC with Decoherence and Opposite Arcs")
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.grid(True)

# Main ROC circle
ax.plot(np.cos(theta_vals), np.sin(theta_vals), color='gray', linestyle='--', alpha=0.3, label="Main ROC Boundary")

# Smaller shifted ROC circle
ax.plot(np.real(roc_small_circle), np.imag(roc_small_circle), color='purple', linestyle='--', alpha=0.5, label="Smaller ROC (shifted π/4)")

# Decohered arc on main ROC
ax.plot(np.real(arc_decoherence), np.imag(arc_decoherence), color='orange', linewidth=3, label="Decoherence Arc (Main ROC)")

# Opposite arc on main ROC
ax.plot(np.real(arc_opposite), np.imag(arc_opposite), color='green', linewidth=3, alpha=0.6, label="Opposite Arc (Main ROC)")

# Tangent vector at decoherence midpoint on main ROC
ax.arrow(np.real(point_tangent), np.imag(point_tangent),
         np.real(tangent_vec), np.imag(tangent_vec),
         head_width=0.05, color='red', label="Tangent (Max Derivative)")

# Entangled particles A and B on main ROC
ax.plot(np.real(pos_A), np.imag(pos_A), 'ro', label="Particle A (Decohered)")
ax.plot(np.real(pos_B), np.imag(pos_B), 'bo', label="Particle B (Opposite)")

# Connect A and B
ax.plot([np.real(pos_A), np.real(pos_B)], [np.imag(pos_A), np.imag(pos_B)],
        linestyle=':', color='purple', alpha=0.7, label="Entangled Correlation")

# Origin
ax.plot(0, 0, 'ko')

ax.legend()
plt.tight_layout()
plt.show()
