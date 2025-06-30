import random
from collections import Counter

def simulate_draws(dataset, target_permutations, trials=100):
    counts = Counter()
    perm_length = len(target_permutations[0])  # Ensure draw length matches permutation length
    for _ in range(trials):
        draw = random.choices(dataset, k=perm_length)
        for perm in target_permutations:
            if tuple(draw) == perm: 
                counts["matched"] += 1
                break  # Only break if a match is found
    probability = counts["matched"] / trials
    return counts["matched"], probability

def draw_percentages(dataset, draws=100_000, k=1):
    """
    Simulate random draws from the dataset and return the percentage of times each number is drawn.
    Returns a dict: {number: percentage}
    """
    counts = Counter()
    for _ in range(draws):
        result = random.choices(dataset, k=k)
        counts.update(result)
    total_draws = draws * k
    percentages = {num: (count / total_draws) * 100 for num, count in counts.items()}
    return percentages

def dataset_from_percentages(percentages, total=100):
    """
    Create a dataset list from a {number: percentage} dictionary.
    The sum of percentages should be <= 100.
    """
    dataset = []
    for num, pct in percentages.items():
        count = round((pct / 100) * total)
        dataset.extend([num] * count)
    return dataset


user_percentages = {
    1: 45, 
    2: 50, 
    3: 5
}
target_permutations = [
    (1, 2), (2, 1),
]

dataset = dataset_from_percentages(user_percentages, total=100)
percentages = draw_percentages(dataset, draws=100_000, k=1)

# Theoretical probability calculation
p1 = user_percentages[1] / 100
p2 = user_percentages[2] / 100
theoretical_prob = p1 * p2 + p2 * p1
print(f"Theoretical probability of drawing (1,2) or (2,1): {theoretical_prob:.4%}")

matches, probability = simulate_draws(dataset,target_permutations)
print(f"- Total permutations considered: {len(target_permutations)}")
print(f"- Matches in {100:,} trials: {matches}")
print(f"- Estimated probability of drawing one of them: {probability:.4%}")


