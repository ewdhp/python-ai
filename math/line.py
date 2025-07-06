"""
Equation of a Line: Table, Plot, and Explanation

This script demonstrates the equation of a line (y = mx + b) with:
- A table of x, y, m*x, and b
- A plot of the line
- Brief descriptions of each variable
"""
import numpy as np
import matplotlib.pyplot as plt

# Description of variables
print("""
Equation of a Line: y = m*x + b

Variables:
  x: Independent variable (input)
  y: Dependent variable (output)
  m: Slope (rate of change of y with respect to x)
  b: Intercept (value of y when x = 0)
""")

# Example values
m = 1.5  # Slope
b = 2    # Intercept
x = np.arange(0, 6, 1)
y = m * x + b

# Table
print(f"{'x':>3} {'m*x':>6} {'b':>4} {'y':>6}")
for xi, yi in zip(x, y):
    print(f"{xi:>3} {m*xi:>6.2f} {b:>4.2f} {yi:>6.2f}")

# Plot
plt.plot(x, y, marker='o', label='y = m*x + b')
plt.title('Equation of a Line')
plt.xlabel('x (independent variable)')
plt.ylabel('y (dependent variable)')
plt.grid(True)
plt.legend()
plt.show()
