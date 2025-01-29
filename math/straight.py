import numpy as np
from itertools import permutations

# Function to generate random integer data
def generate_random_data_int(size, low=0, high=10):
    return np.random.randint(low, high, size)  # Generates random integers between low and high (inclusive)

# Function to compare permutations of ai to windows in the signal
def compare(signal, window_size, ai, threshold=90):
    matches = []  # To store positions where pattern matches
    pattern_found = False  # To track if a match is found
    matched_positions = set()  # Use set to store unique matched positions
    
    # Generate all permutations of the pattern ai
    window_permutations = list(permutations(ai))
    
    # Loop over all positions in the signal
    for i in range(len(signal) - window_size + 1):
        window = signal[i:i + window_size]
        
        # Compare each permutation of the pattern to the window
        for perm in window_permutations:
            # Convert both perm and window to NumPy arrays to avoid data type issues
            perm = np.array(perm, dtype=np.float64)
            window = np.array(window, dtype=np.float64)
            
            # Calculate Euclidean distance between the window and the permutation
            distance = np.linalg.norm(perm - window)
            
            # Calculate percentage match based on distance
            match_percentage = (1 / (1 + distance)) * 100  # Normalizing to get a percentage
            
            # If the match is above the threshold, consider it a match
            if match_percentage >= threshold:
                matches.append((i, perm, match_percentage))
                pattern_found = True
                # Add the matched position to the set
                matched_positions.add(i)
    
    # Return matches, whether a pattern was found, and the matched positions
    return matches, pattern_found, matched_positions

# Function to summarize matches and print a summary
def run(window_size, ai, threshold=90, n=10, total_data_size=100):
    total_matches = 0
    matched_patterns_percent = 0
    unique_matched_positions = set()  # To track unique positions across all runs

    # Loop for n comparisons
    for run in range(n):
        print(f"Run {run + 1}:")
        
        # Regenerate the signal for each run to ensure randomness
        signal = generate_random_data_int(total_data_size)
        
        # Print the generated signal for debugging purposes
        #print(f"Generated Signal: {signal[:30]} ...")  # Only print the first 30 elements to avoid too much output
        
        # Perform the comparison with the generated signal
        matches, pattern, matched = compare(signal, window_size, ai, threshold)

        # Print results for this run
        if pattern:
            #print(f"Pattern found in the following windows (Total matches: {len(matches)}):")
            for match in matches:
                index, perm, percentage = match
                #print(f"At position {index}, permutation {perm} has {percentage:.2f}% match")
            
            # Add the matched positions to the global set (unique matches across all runs)
            unique_matched_positions.update(matched)
        else:
            print("No pattern found.")

    
    # Calculate total number of unique matched positions
    total_matches = len(unique_matched_positions)
    
    # Calculate percentage of matches relative to the total data size
    if total_data_size > 0:
        matched_patterns_percent = (total_matches / total_data_size) * 100
    
    # Print final summary
    print("\nSummary of All Runs:")
    print(f"Total number of unique matched patterns: {total_matches}")
    print(f"Matched patterns as percentage of data: {matched_patterns_percent:.2f}%")
    print(f"Total data size: {total_data_size}")
    print(f"Indices of matched patterns: {sorted(unique_matched_positions)}")

ai = np.array([0,5,3,7,9])
window_size = len(ai)
run(window_size, ai, threshold=90, n=3, total_data_size=1000)