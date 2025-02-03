import sympy as sp

# Define the symbol
x = sp.symbols('x')

# Define your polynomial, for example:
P = 2 * x**2 + 2 * x + 1  # You can change this polynomial as needed.

# Calculate the even and odd parts using the formulas
P_even = sp.simplify((P + P.subs(x, -x)) / 2)
P_odd = sp.simplify((P - P.subs(x, -x)) / 2)

# Display the results
print("Original polynomial:")
sp.pprint(P)
print("\nEven part:")
sp.pprint(P_even)
print("\nOdd part:")
sp.pprint(P_odd)
