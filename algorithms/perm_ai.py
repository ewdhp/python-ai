import random
from collections import Counter
from itertools import permutations as it_permutations

def simulate_draws(dataset, target_permutations, trials=100_000):
    """
    Simulate random draws from the dataset and count how many times
    a draw matches any of the target permutations.
    Returns a tuple: (number of matches, estimated probability)
    """
    counts = Counter()
    perm_length = len(target_permutations[0])  # Ensure draw length matches permutation length
    for _ in range(trials):
        draw = random.choices(dataset, k=perm_length)
        for perm in target_permutations:
            if tuple(draw) == perm: 
                counts["matched"] += 1
                break  # Only break if a match is found
    probability = counts["matched"] / trials
    return counts["matched"], probability  # <-- Return both values

def draw_percentages(dataset, draws=100_000, k=1):
    """
    Simulate random draws from the dataset and return the 
    percentage of times each number is drawn.
    Returns a dict: {number: percentage}
    """
    counts = Counter()
    for _ in range(draws):
        result = random.choices(dataset, k=k)
        counts.update(result)
    total_draws = draws * k
    percentages = {num: (count / total_draws) * 100 for num, count in counts.items()}
    return percentages  # <-- Only return percentages

def create_dataset(percentages, total=None, return_probs=False):
    """
    Create a dataset list from a {number: percentage} dictionary.
    If total is None, use the sum of all values in percentages as the total.
    Optionally return the probability of each number as a dict.
    """
    if total is None:
        total = sum(percentages.values())
    dataset = []
    for num, pct in percentages.items():
        count = round((pct / 100) * total) if max(percentages.values()) > 1 else round(pct)
        dataset.extend([num] * count)
    if return_probs:
        total_count = len(dataset)
        probs = {num: dataset.count(num) / total_count for num in percentages}
        return dataset, probs
    return dataset

def theoretical_probability(permutations, probs):
    """
    Compute the theoretical probability of drawing any permutation from the given probabilities.
    Assumes draws are with replacement and independent.
    """
    prob = 0
    for perm in permutations:
        p = 1
        for num in perm:
            p *= probs.get(num, 0)
        prob += p
    return prob

def generate_permutations(numbers, length=2):
    """
    Generate all possible ordered permutations 
    of the given numbers with the specified length.
    """
    return list(it_permutations(numbers, length))

def select_permutations(numbers, custom_permutations=None, length=2):
    """
    If custom_permutations is provided and has length > 0, use it.
    Otherwise, generate all possible ordered permutations of the given numbers with the specified length.
    """
    if custom_permutations and len(custom_permutations) > 0:
        return custom_permutations
    return generate_permutations(numbers, length)

d = {
    1: 50, 
    2: 50, 
}

# Optionally provide custom permutations, or leave as empty list to auto-generate
custom_permutations = []  # e.g. [(1,2), (2,1)]

p = select_permutations(d.keys(), custom_permutations, length=2)

dataset_list, probs = create_dataset(d, total=sum(d.values()), return_probs=True)
percentages = draw_percentages(dataset_list, draws=100_000, k=1)
matches, probability = simulate_draws(dataset_list, p)  # <-- Now works, returns two values
theoretical_prob = theoretical_probability(p, probs)

print(f"\nTheoretical probability: {theoretical_prob:.4%}\n")
print(f"- Total permutations: {len(p)}")
print(f"- Matches in {100_000:,} trials: {matches}")
print(f"- Estimated probability of drawing: {probability:.4%}\n")


