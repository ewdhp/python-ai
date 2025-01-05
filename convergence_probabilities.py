import numpy as np
import matplotlib.pyplot as plt

# Set the random seed for reproducibility
np.random.seed(42)

# Parameters
num_trials = 100  # Total number of coin flips
num_simulations = 100  # Number of simulations
prob_head = 0.5  # Probability of getting heads in a fair coin flip

# Function to simulate a sequence of coin flips (Bernoulli trials)
def simulate_coin_flips(n):
    return np.random.binomial(1, prob_head, n)

# Function for almost sure convergence (Sample mean of coin flips)
def almost_sure_convergence(num_trials, num_simulations):
    means = []
    for _ in range(num_simulations):
        flips = simulate_coin_flips(num_trials)
        mean = np.cumsum(flips) / np.arange(1, num_trials + 1)  # Cumulative mean of flips
        means.append(mean)
    return np.array(means)

# Function for convergence in probability (Proportion of heads)
def convergence_in_probability(num_trials, num_simulations, epsilon=0.05):
    proportions = []
    for _ in range(num_simulations):
        flips = simulate_coin_flips(num_trials)
        proportion = np.cumsum(flips) / np.arange(1, num_trials + 1)
        # Calculate the probability that the proportion is within epsilon of 0.5
        probability = np.mean(np.abs(proportion - 0.5) < epsilon)
        proportions.append(probability)
    return np.array(proportions)

# Simulate almost sure convergence (Cumulative mean)
means = almost_sure_convergence(num_trials, num_simulations)

# Simulate convergence in probability (Proportion of heads within epsilon)
proportions = convergence_in_probability(num_trials, num_simulations)

# Plotting Almost Sure Convergence (Cumulative Mean)
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
for mean in means:
    plt.plot(mean, alpha=0.3)  # Each simulation
plt.axhline(0.5, color='red', linestyle='--', label='True Mean (0.5)')
plt.title('Almost Sure Convergence (Cumulative Mean)')
plt.xlabel('Number of Trials')
plt.ylabel('Cumulative Mean')
plt.legend()

# Plotting Convergence in Probability (Proportion of heads within epsilon)
plt.subplot(1, 2, 2)
plt.plot(np.mean(proportions, axis=0), label='Proportion Within Epsilon', color='blue')
plt.axhline(1, color='red', linestyle='--', label='Convergence in Probability (1)')
plt.title('Convergence in Probability (Proportion of Heads within epsilon)')
plt.xlabel('Number of Trials')
plt.ylabel('Proportion Within Epsilon')
plt.legend()

plt.tight_layout()
plt.show()
