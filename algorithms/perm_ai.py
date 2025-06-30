import random
from collections import Counter

def simulate_draws(trials=100_000):
    counts = Counter()
    for _ in range(trials):
        draw = random.choices(dataset, k=4)
        for perm in target_permutations:
            if tuple(draw) == perm: 
                counts["matched"] += 1
            break
    probability = counts["matched"] / trials
    return counts["matched"], probability

# AI dataset
dataset = [
    5, 1, 6, 8, 6, 9, 6, 
    8, 4, 1, 4, 4, 5, 7, 
    5, 1, 2, 4, 7, 2, 2, 
    4, 8, 5, 7, 5, 4, 6, 
    2, 5, 4, 5, 3, 7, 8
]

 # % square root aprox mean, left one coeeff to get only
target_permutations = [( 5,6,7,4)] 
matches, probability = simulate_draws()

print("\nSummary:")
print(f"- Total permutations considered: {len(target_permutations)}")
print(f"- Matches in {100_000:,} trials: {matches}")
print(f"- Estimated probability of drawing one of them: {probability:.4%}")
