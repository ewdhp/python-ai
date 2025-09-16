import numpy as np
import matplotlib.pyplot as plt

# Parameters
wavelength = 0.5
k = 2 * np.pi / wavelength  # wave number
aperture_points = 50
aperture_width = 10
screen_points = 200
screen_range = 20

# 1. Geometric Huygens circles -------------------
x_aperture = np.linspace(-aperture_width/2, aperture_width/2, aperture_points)

# Points on the screen (far-field approx.)
x_screen = np.linspace(-screen_range/2, screen_range/2, screen_points)

# Complex field contributions
field = np.zeros_like(x_screen, dtype=complex)

for x0 in x_aperture:
    r = np.sqrt((x_screen - x0)**2 + 50**2)  # distance from aperture to screen
    contrib = np.exp(1j * k * r) / r
    field += contrib

intensity = np.abs(field)**2

# 2. Phasor diagram (sum contributions tip-to-tail) -----
phasors = []
sum_phasor = 0
for x0 in x_aperture:
    r = np.sqrt((0 - x0)**2 + 50**2)  # on-axis observation
    contrib = np.exp(1j * k * r) / r
    sum_phasor += contrib
    phasors.append(sum_phasor)

phasors = np.array(phasors)

# ---- Plotting ----
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# (1) Huygens circles
for x0 in x_aperture[::5]:  # plot fewer for clarity
    circle = plt.Circle((x0, 0), 5, fill=False, color="blue", alpha=0.3)
    axes[0].add_patch(circle)
axes[0].set_xlim(-aperture_width, aperture_width)
axes[0].set_ylim(-1, 6)
axes[0].set_aspect("equal")
axes[0].set_title("Huygens wavelets (geometric picture)")
axes[0].set_xlabel("Aperture")
axes[0].set_ylabel("Propagation")

# (2) Phasor diagram
axes[1].plot(phasors.real, phasors.imag, "-o", color="purple")
axes[1].set_aspect("equal", "box")
axes[1].set_title("Phasor sum (complex exponentials)")
axes[1].set_xlabel("Re")
axes[1].set_ylabel("Im")

# (3) Diffraction pattern
axes[2].plot(x_screen, intensity, color="red")
axes[2].set_title("Diffraction pattern (intensity)")
axes[2].set_xlabel("Screen position")
axes[2].set_ylabel("Intensity")

plt.tight_layout()
plt.show()
