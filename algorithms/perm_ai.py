import random
from collections import Counter
from itertools import permutations as it_permutations
import time
import os
import fractions

def simulate_draws(dataset, target_permutations, trials=100):
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

def draw_percentages(dataset, draws=100, k=1):
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

def create_dataset(percentages, total=None, return_probs=True):
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

def select_permutations(numbers, custom_permutations=None, length=None):
    """
    If custom_permutations is provided and has length > 0, use it.
    Otherwise, generate all possible ordered permutations of the given numbers with the specified length.
    If length is not provided, infer it from custom_permutations or use len(numbers).
    """
    if custom_permutations and len(custom_permutations) > 0:
        # Infer length from the first custom permutation if not provided
        inferred_length = len(custom_permutations[0]) if custom_permutations else len(numbers)
        return custom_permutations if length is None or length == inferred_length else [
            perm for perm in custom_permutations if len(perm) == length
        ]
    # If length is not provided, use len(numbers)
    if length is None:
        length = len(numbers)
    return generate_permutations(numbers, length)

def format_probability_fraction(prob, perm, probs):
    # Compute the probability for a single permutation as a fraction
    p = 1
    for num in perm:
        p *= probs.get(num, 0)
    if p > 0:
        frac = fractions.Fraction(p).limit_denominator()
        return f"{frac.numerator}/{frac.denominator}", p * 100
    return "-", 0

def print_permutation_table(permutations, probs):
    print("\nPermutation | Theoretical Probability (fraction) | Theoretical Probability (%)")
    print("-" * 65)
    for perm in permutations:
        frac, pct = format_probability_fraction(None, perm, probs)
        perm_str = ",".join(str(x) for x in perm)
        print(f"{perm_str:<11} | {frac:^33} | {pct:>8.4f}%")
    print("-" * 65)

dataset_file = "dataset.txt"
if os.path.exists(dataset_file):
    d = {}
    with open(dataset_file, "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) == 2:
                try:
                    key = int(parts[0].strip())
                    value = float(parts[1].strip())
                    d[key] = value
                except ValueError:
                    continue
else:

    d = {
        1: 50, 
        2: 50,
    }

dataset, probs = create_dataset(d, total=sum(d.values()))

while True:
    print("\nEnter permutations as comma-separated numbers.")
    print("Press Enter on an empty line to finish" + 
        ", or type 'q' or 'exit' to quit.\n")
    user_permutations = []
    while True:
        inp = input("Permutation: ").strip()
        if inp.lower() in ("exit", "q"):
            print("Exiting.")
            exit()
        if not inp:
            break
        try:
            perms = inp.split()
            for perm_str in perms:
                perm = tuple(
                    int(x.strip()) 
                    for x in perm_str.split(",") 
                    if x.strip())
                if perm:  # Only add non-empty permutations
                    user_permutations.append(perm)
        except Exception:
            print("Invalid input, try again.")

        # Print summary after each user prompt 
        # (if at least one permutation entered)
        if user_permutations:
            start_time = time.time()
            k = len(user_permutations[0])
            p = select_permutations(d.keys(), user_permutations, length=k)
            theoretical_prob = theoretical_probability(p, probs)       
            percentages = draw_percentages(dataset, draws=100, k=k)                       
            matches, probability = simulate_draws(dataset, p)
            elapsed = time.time() - start_time    
            print_permutation_table(p, probs)
            print(f"\n- Theoretical probability: {theoretical_prob:.4%}")
            print(f"- Total permutations: {len(p)}")
            print(f"- Matches in {100_000:,} trials: {matches}")
            print(f"- Estimated probability of drawing: {probability:.4%}\n")
            print(f"Time elapsed: {elapsed:.2f} seconds\n")
            user_permutations = []  # <-- Reset after summary

    if not user_permutations:
        print("No permutations entered. Exiting.")
        break
