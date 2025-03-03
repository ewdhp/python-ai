import numpy as np

# Dataset
x = np.array([1, 2, 3, 4])
y = np.array([2, 3, 4, 5])

# Number of training examples
m = len(x)

# Parameters
theta_0 = 0
theta_1 = 1

def compute_cost(x, y, theta_0, theta_1):
    m = len(x)
    total_cost = 0
    for i in range(m):
        prediction = theta_0 + theta_1 * x[i]
        total_cost += (prediction - y[i]) ** 2
    return total_cost / (2 * m)

def gradient_descent(x, y, theta_0, theta_1, alpha, iterations):
    m = len(x)
    for _ in range(iterations):
        sum_errors_0 = 0
        sum_errors_1 = 0
        for i in range(m):
            prediction = theta_0 + theta_1 * x[i]
            error = prediction - y[i]
            sum_errors_0 += error
            sum_errors_1 += error * x[i]
        
        theta_0 -= (alpha / m) * sum_errors_0
        theta_1 -= (alpha / m) * sum_errors_1
    
    return theta_0, theta_1

# Hyperparameters
alpha = 0.01
iterations = 10000

theta_0, theta_1 = gradient_descent(x, y, theta_0, theta_1, alpha, iterations)

print(f"Final parameters: theta_0 = {theta_0}, theta_1 = {theta_1}")
cost = compute_cost(x, y, theta_0, theta_1)
print(f"Final cost: {cost}")

