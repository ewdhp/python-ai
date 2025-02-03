import math

def tan_taylor_series(x, terms):
    # Coefficients for the first 10 terms
    coefficients = [
        1, 
        1/3, 
        2/15, 
        17/315, 
        62/2835, 
        1382/155925, 
        21844/6081075, 
        929569/638512875, 
        6404582/10854718875, 
        443861162/1856156927625
    ]
    
    tan_approximation = 0
    for n in range(terms):
        term = coefficients[n] * x**(2*n + 1)
        tan_approximation += term
        print(f"Term {n + 1}: {term}")
    return tan_approximation

# Example usage
x = math.pi / 4  # Change the value of x as needed
terms = 10  # Number of terms in the Taylor series
result = tan_taylor_series(x, terms)
print(f"The approximation of tan({x}) using the Taylor series up to the 10th term is: {result}")
