import numpy as np
from itertools import permutations
from scipy.signal import convolve

# Function to generate random integer data
def generate_random_data_int(size, low=0, high=10):
    return np.random.randint(low, high, size)  # Generates random integers between low and high (inclusive)

# Function to compare permutations of ai to windows in the signal using convolution
def compare(signal, window_size, ai, threshold=90):
    matches = []  # To store positions where pattern matches
    pattern_found = False  # To track if a match is found
    matched_positions = {}  # Use dictionary to store unique matched positions and their sequences
    
    # Normalize the pattern ai
    ai = np.array(ai, dtype=np.float64)
    ai_mean = np.mean(ai)
    ai_std = np.std(ai)
    ai_normalized = (ai - ai_mean) / ai_std
    
    # Normalize the signal
    signal = np.array(signal, dtype=np.float64)
    signal_mean = np.mean(signal)
    signal_std = np.std(signal)
    signal_normalized = (signal - signal_mean) / signal_std
    
    # Perform convolution
    conv_result = convolve(signal_normalized, ai_normalized[::-1], mode='valid')
    
    # Loop over the convolution result to find matches
    for i in range(len(conv_result)):
        match_percentage = (conv_result[i] / window_size) * 100  # Normalize to get a percentage
        
        # If the match is above the threshold, consider it a match
        if match_percentage >= threshold:
            matches.append((i, ai, match_percentage))
            pattern_found = True
            # Add the matched position and sequence to the dictionary
            matched_positions[i] = signal[i:i + window_size]
            print(f"Match found at index {i}: {signal[i:i + window_size]}")  # Debug print
    
    # Return matches, whether a pattern was found, and the matched positions with sequences
    return matches, pattern_found, matched_positions

# Function to summarize matches and print a summary
def run(window_size, ai, threshold, n, total_data_size):
    total_matches = 0
    matched_patterns_percent = 0
    unique_matched_positions = {}  # To track unique positions and sequences across all runs

    # Loop for n comparisons
    for run in range(n):
        # Regenerate the signal for each run to ensure randomness
        signal = generate_random_data_int(total_data_size)
        
        print(signal)

        # Perform the comparison with the generated signal
        matches, pattern, matched = compare(signal, window_size, ai, threshold)
        # Print results for this run
        if pattern:
            print(f"Run: {run + 1}, Total matches: {len(matches)}, Matched pattern indices: {list(matched.keys())}")
            for match in matches:
                index, perm, percentage = match
                sequence = signal[index:index + window_size]
            
            # Add the matched positions and sequences to the global dictionary (unique matches across all runs)
            unique_matched_positions.update(matched)
        else:
            print(f"Run: {run + 1}, No pattern found.")

    # Calculate total number of unique matched positions
    total_matches = len(unique_matched_positions)
    
    # Calculate percentage of matches relative to the total data size
    if total_data_size > 0:
        matched_patterns_percent = (total_matches / total_data_size) * 100
    
    # Print final summary
    print("\n\nSUMMARY OF ALL RUNS.\n")
    print(f"Total data size: {total_data_size}")
    print(f"Total number of unique matched patterns: {total_matches}")
    print(f"Matched patterns as percentage of data: {matched_patterns_percent:.2f}%")
   
    print(f"Indices of matched patterns: {sorted(unique_matched_positions.keys())}\n")
    
    # Print the sequences starting from each matched index
    for index in sorted(unique_matched_positions.keys()):
        sequence = unique_matched_positions[index]
        print(f"Sequence starting at index {index}: {sequence}")

    # Check for geometric progression or power series in matched patterns
    check_series_patterns(unique_matched_positions)

# Function to preprocess the sequence
def preprocess_sequence(sequence):
    # Remove consecutive identical values
    cleaned_sequence = [sequence[0]]
    for i in range(1, len(sequence)):
        if sequence[i] != sequence[i - 1]:
            cleaned_sequence.append(sequence[i])
    return cleaned_sequence

# Function to check if a sequence is a geometric progression
def is_geometric_progression(sequence):
    if len(sequence) < 3:
        return False
    ratio = sequence[1] / sequence[0] if sequence[0] != 0 else 0
    print(f"Checking geometric progression for sequence: {sequence}, ratio: {ratio}")  # Debug print
    for i in range(1, len(sequence)):
        if sequence[i - 1] == 0 or sequence[i] / sequence[i - 1] != ratio:
            return False
    return True

# Function to check if a sequence is a power series
def is_power_series(sequence):
    if len(sequence) < 3:
        return False
    base = sequence[1] / sequence[0] if sequence[0] != 0 else 0
    print(f"Checking power series for sequence: {sequence}, base: {base}")  # Debug print
    for i in range(1, len(sequence)):
        if sequence[i] != sequence[0] * (base ** i):
            return False
    return True

# Function to check for geometric progression or power series in matched patterns
def check_series_patterns(matched_positions):
    geometric_progression_sequences = []
    power_series_sequences = []
    for sequence in matched_positions.values():
        cleaned_sequence = preprocess_sequence(sequence)
        print(f"Checking sequence: {cleaned_sequence}")  # Debug print
        if is_geometric_progression(cleaned_sequence):
            print(f"Geometric progression found: {cleaned_sequence}")  # Debug print
            geometric_progression_sequences.append(sequence)
        if is_power_series(cleaned_sequence):
            print(f"Power series found: {cleaned_sequence}")  # Debug print
            power_series_sequences.append(sequence)
    
    # Print the results
    print("\nGeometric progression sequences:", geometric_progression_sequences)
    print("Power series sequences:", power_series_sequences)
    
    # Print the sequences for verification
    print("\nSequences for geometric progression:")
    for sequence in geometric_progression_sequences:
        print(sequence)
    
    print("\nSequences for power series:")
    for sequence in power_series_sequences:
        print(sequence)

print("\n")
n = 1
threshold = 100
total_data_size = 100
ai = np.array([1, 2, 4])
window_size = len(ai)
run(window_size, ai, threshold, n, total_data_size)
print("\n")