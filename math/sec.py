import numpy as np
import matplotlib.pyplot as plt

# Define the x values
x = np.linspace(-1, 1, 1000)

# Define the tangent function and its derivative (sec^2(x))
tan_y = np.tan(x)

tan_derivative_y = np.cos(x) # sec^2(x)



# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x, tan_y, label='tan(x)', color='blue')
plt.plot(x, tan_derivative_y, label="Derivative of tan(x) (sec^2(x))", color='red', linestyle='--')

# Add vertical lines at the asymptotes
for i in range(-2, 3):
    plt.axvline(x=i * np.pi / 2, color='gray', linestyle=':', linewidth=0.8)

# Add labels, legend, and title
plt.title('Tangent Function and Its Derivative')
plt.xlabel('x')
plt.ylabel('y')
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
plt.legend()
plt.grid()

# Show the plot
plt.show()