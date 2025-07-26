import numpy as np
import matplotlib.pyplot as plt

# Define a convex function and a non-convex function
def convex_f(x):
    return x**2

def nonconvex_f(x):
    return -x**2 + 1  # Concave (not convex)

x = np.linspace(-2, 2, 200)
y_convex = convex_f(x)
y_nonconvex = nonconvex_f(x)

# Pick two points for both functions
x1, x2 = -1.5, 1.0
y1_convex, y2_convex = convex_f(x1), convex_f(x2)
y1_nonconvex, y2_nonconvex = nonconvex_f(x1), nonconvex_f(x2)

# Compute the convex combination for t in [0, 1]
t = np.linspace(0, 1, 100)
x_t = t * x1 + (1 - t) * x2
y_t_convex = t * y1_convex + (1 - t) * y2_convex
y_t_nonconvex = t * y1_nonconvex + (1 - t) * y2_nonconvex

fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# --- Convex function plot ---
axs[0].plot(x, y_convex, label='Convex $f(x) = x^2$')
axs[0].scatter([x1, x2], [y1_convex, y2_convex], color='red', zorder=5, label='Points on $f(x)$')
axs[0].plot(x_t, y_t_convex, 'g--', label='Chord between points')
axs[0].plot(x_t, convex_f(x_t), 'b:', label='$f(tx_1 + (1-t)x_2)$')
# Shade area between function and chord
axs[0].fill_between(x_t, convex_f(x_t), y_t_convex, where=(convex_f(x_t) < y_t_convex), color='yellow', alpha=0.3, label='Function below chord')
axs[0].set_title('Convex Function')
axs[0].set_xlabel('x')
axs[0].set_ylabel('f(x)')
axs[0].legend()
axs[0].grid(True)
axs[0].annotate('Function always below chord', xy=(0, convex_f(0)), xytext=(-1.5, 2),
                arrowprops=dict(facecolor='black', arrowstyle='->'), fontsize=10, color='black')

# --- Non-convex function plot ---
axs[1].plot(x, y_nonconvex, label='Non-convex $f(x) = -x^2 + 1$')
axs[1].scatter([x1, x2], [y1_nonconvex, y2_nonconvex], color='red', zorder=5, label='Points on $f(x)$')
axs[1].plot(x_t, y_t_nonconvex, 'g--', label='Chord between points')
axs[1].plot(x_t, nonconvex_f(x_t), 'b:', label='$f(tx_1 + (1-t)x_2)$')
# Shade area where function is above the chord
axs[1].fill_between(x_t, nonconvex_f(x_t), y_t_nonconvex, where=(nonconvex_f(x_t) > y_t_nonconvex), color='orange', alpha=0.3, label='Function above chord')
axs[1].set_title('Non-Convex Function')
axs[1].set_xlabel('x')
axs[1].set_ylabel('f(x)')
axs[1].legend()
axs[1].grid(True)
axs[1].annotate('Function above chord (not convex)', xy=(0, nonconvex_f(0)), xytext=(-1.5, 1.5),
                arrowprops=dict(facecolor='black', arrowstyle='->'), fontsize=10, color='black')

plt.suptitle('Convex vs Non-Convex Visualization')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()