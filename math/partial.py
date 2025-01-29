import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

# Define the arctan function
x = np.linspace(-10, 10, 1000)
y = np.arctan(x)

# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(x, y, label=r'$\arctan(x)$', color='blue')

# Add labels, title, and legend
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
plt.title('Plot of the Arctangent Function')
plt.xlabel('x')
plt.ylabel(r'$\arctan(x)$')
plt.grid(alpha=0.3)
plt.legend()

# Show the plot
plt.show()
