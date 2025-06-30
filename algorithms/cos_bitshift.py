import time
import math
import numpy as np

class Quantize3DLayer:
    def __init__(self, scale=1024):
        self.scale = scale  # Fixed-point scale

    def forward(self, tensor):
        # tensor shape: (depth, height, width)
        x_int = (tensor * self.scale).astype(np.int32)
        x2 = (x_int * x_int) >> 10
        x4 = (x2 * x2) >> 10
        term1 = x2 >> 1
        term2 = x4 // 24
        y_int = self.scale - term1 + term2
        return y_int.astype(np.float32) / self.scale

    def backward(self, tensor):
        # Returns approximate derivative per element
        x_int = (tensor * self.scale).astype(np.int32)
        x2 = (x_int * x_int) >> 10
        x3 = (x_int * x2) >> 10
        dy_int = -x_int + (x3 // 6)
        return dy_int.astype(np.float32) / self.scale

# Standard cosine + derivative
def classic_cos_with_gradient(x):
    cos_val = math.cos(x)
    deriv_val = -math.sin(x)
    return cos_val, deriv_val

# Bit-shift cosine + derivative approximation (fixed-point)
def cosine_with_gradient(x_int, scale=1024):
    x2 = (x_int * x_int) >> 10
    x4 = (x2 * x2) >> 10
    term1 = x2 >> 1
    term2 = x4 // 24
    cos_approx = scale - term1 + term2
    x3 = (x_int * x2) >> 10
    deriv_approx = -x_int + (x3 // 6)
    return cos_approx, deriv_approx

# Main timing function
def main():
    iterations = 100_000
    theta = math.pi / 90  # for float version
    scale = 1024
    theta_fixed = int(theta * scale)

    # Time classic math library version
    start = time.perf_counter()
    for _ in range(iterations * 1000):
        classic_cos_with_gradient(theta)
    t_classic = time.perf_counter() - start

    # Time bit-shift fixed-point version
    start = time.perf_counter()
    for _ in range(iterations):
        cosine_with_gradient(theta_fixed, scale)
    t_bitshift = time.perf_counter() - start

    print(f"Classic math version:     {t_classic:.6f} seconds")
    print(f"Bit-shift fixed-point:    {t_bitshift:.6f} seconds")

if __name__ == "__main__":
    main()
