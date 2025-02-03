import math

def approximate_e(n):
    sum = 0
    for k in range(n + 1):
        term = 1 / math.factorial(k)
        sum += term
    return sum

# Example usage
n = 1 
result = approximate_e(n)
print(f"The approximation for e is: {result}")
