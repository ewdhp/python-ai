import math

def sin_taylor(x, n):
    sin_sum = 0
    for k in range(n):
        term = ((-1)**k * x**(2*k + 1)) / math.factorial(2*k + 1)
        sin_sum += term
    return sin_sum

def cos_taylor(x, n):
    cos_sum = 0
    for k in range(n):
        term = ((-1)**k * x**(2*k)) / math.factorial(2*k)
        cos_sum += term
    return cos_sum

def tan_taylor(x, n):
    sin_approx = sin_taylor(x, n)
    cos_approx = cos_taylor(x, n)
    return sin_approx / cos_approx

# Example usage
x = math.pi / 4  # Change the value of x as needed
n = 10  # Change the value of n for more accuracy
result = tan_taylor(x, n)
print(f"The approximation of tan({x}) using Taylor series is: {result}")
