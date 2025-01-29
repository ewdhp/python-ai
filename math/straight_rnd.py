import numpy as np
from itertools import permutations

# Function to generate random integer data
def generate_random_data_int(size, low=0, high=10):
    return np.random.randint(low, high, size)  # Generates random integers between low and high (inclusive)

# Function to compare permutations of ai to windows in the signal
def compare_window_to_signal(signal, window_size, ai, threshold=90):
    matches = []  # To store positions where pattern matches
    pattern_found = False  # To track if a match is found
    matched_positions = {}  # To store matched positions with percentages
    
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
                # Store the matched position and percentage in the dictionary
                matched_positions[i] = match_percentage
    
    # Return matches, whether a pattern was found, and the matched positions
    return matches, pattern_found, matched_positions


# Predefined pattern ai (e.g., a small template or reference pattern)
ai = np.array([0,1,2,3])
window_size = len(ai)

# Generate a random data array (size 15 for example)
signal = generate_random_data_int(100)
print(f"Random Data:\n {signal} \n")

# Call the function and detect patterns
matches, pattern_found, matched_positions = compare_window_to_signal(signal, window_size, ai)

# Output results
if pattern_found:
    print("Pattern found in the following windows:")
    for match in matches:
        index, perm, percentage = match
        print(f"At position {index}, permutation {perm} has {percentage:.2f}% match")
    
    # Output matched positions and percentages
    print("\nMatched Positions and Percentages:")
    for pos, percentage in matched_positions.items():
        print(f"Position {pos} has {percentage:.2f}% match")
else:
    print("No pattern found.")
