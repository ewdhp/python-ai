import numpy as np

# Given sequences and their starting indices
sequences = {
    2281: [0., 0., 0., 7., 8., 9., 9., 3., 1., 3., 1.],
    3957: [0., 0., 0., 2., 9., 7., 8., 9., 7., 1., 0.],
    3958: [0., 0., 2., 9., 7., 8., 9., 7., 1., 0., 3.],
    7414: [0., 3., 8., 5., 9., 9., 9., 8., 8., 0., 2.],
    8423: [3., 0., 7., 7., 9., 9., 9., 9., 4., 4., 0.],
    9791: [0., 0., 9., 7., 4., 9., 9., 8., 6., 1., 0.],
    9857: [0., 0., 1., 7., 8., 9., 9., 6., 6., 2., 2.],
    10393: [0., 5., 5., 4., 8., 9., 8., 6., 3., 0., 0.],
    16886: [0., 1., 6., 9., 5., 9., 7., 6., 1., 0., 1.],
    19043: [0., 2., 0., 8., 7., 8., 9., 8., 3., 1., 0.],
    19990: [0., 3., 7., 6., 9., 9., 9., 7., 5., 3., 0.],
    23288: [1., 2., 0., 8., 6., 9., 8., 5., 1., 0., 1.],
    23300: [0., 2., 3., 6., 9., 8., 9., 6., 4., 0., 0.],
    24798: [1., 1., 7., 9., 9., 8., 7., 6., 0., 1., 0.],
    25874: [0., 0., 2., 9., 9., 7., 9., 9., 2., 9., 0.],
    30234: [0., 0., 3., 6., 8., 9., 7., 5., 8., 0., 2.],
    31706: [5., 0., 2., 5., 9., 9., 8., 9., 3., 0., 0.],
    31707: [0., 2., 5., 9., 9., 8., 9., 3., 0., 0., 3.],
    31980: [1., 1., 1., 4., 9., 9., 9., 4., 8., 0., 1.],
    32273: [1., 0., 7., 7., 8., 9., 8., 2., 9., 0., 0.],
    34131: [0., 2., 2., 7., 9., 8., 6., 8., 1., 0., 1.],
    34571: [0., 0., 0., 3., 6., 9., 9., 7., 1., 3., 0.],
    34692: [0., 3., 5., 4., 9., 9., 9., 9., 1., 3., 2.],
    34775: [1., 2., 0., 9., 7., 8., 8., 8., 2., 0., 1.],
    36649: [0., 2., 7., 9., 8., 9., 9., 4., 3., 0., 2.],
    42368: [0., 1., 3., 9., 9., 8., 9., 8., 9., 1., 1.],
    42369: [1., 3., 9., 9., 8., 9., 8., 9., 1., 1., 0.],
    45326: [0., 1., 3., 5., 9., 9., 9., 4., 2., 5., 1.],
    51562: [2., 1., 2., 7., 8., 9., 7., 7., 3., 0., 0.],
    53535: [0., 2., 9., 9., 9., 9., 8., 1., 0., 4., 0.],
    56662: [1., 0., 3., 8., 9., 9., 8., 4., 0., 3., 0.],
    58141: [1., 2., 2., 4., 8., 9., 9., 5., 0., 0., 0.],
    58676: [0., 1., 3., 6., 8., 9., 6., 9., 3., 4., 0.],
    61033: [1., 0., 1., 5., 9., 9., 9., 9., 2., 0., 2.],
    61034: [0., 1., 5., 9., 9., 9., 9., 2., 0., 2., 2.],
    64477: [1., 0., 5., 1., 9., 9., 5., 9., 1., 0., 0.],
    65154: [0., 0., 2., 4., 9., 8., 9., 9., 4., 0., 4.],
    66872: [1., 0., 0., 6., 6., 9., 8., 9., 5., 3., 0.],
    67126: [0., 1., 5., 9., 9., 9., 5., 7., 7., 3., 0.],
    68869: [0., 3., 7., 9., 7., 9., 8., 6., 9., 1., 0.],
    68948: [1., 0., 5., 5., 9., 9., 9., 5., 9., 1., 2.],
    73078: [0., 0., 8., 7., 9., 9., 7., 4., 8., 1., 0.],
    73717: [1., 0., 5., 5., 8., 8., 9., 6., 5., 0., 0.],
    73850: [0., 0., 2., 9., 8., 9., 6., 8., 2., 0., 4.],
    75198: [0., 0., 1., 6., 9., 9., 6., 7., 4., 5., 0.],
    76406: [0., 1., 6., 6., 8., 8., 9., 5., 9., 2., 0.],
    76700: [4., 0., 8., 9., 9., 9., 7., 6., 0., 1., 0.],
    76915: [1., 0., 3., 5., 9., 9., 9., 5., 4., 1., 3.],
    79286: [2., 0., 8., 8., 9., 9., 7., 7., 2., 4., 0.],
    83528: [0., 0., 3., 9., 8., 9., 9., 9., 5., 0., 4.],
    87913: [1., 1., 1., 6., 9., 9., 9., 7., 0., 2., 3.],
    90478: [0., 6., 8., 9., 6., 9., 9., 9., 2., 0., 0.],
    92536: [1., 0., 3., 1., 9., 9., 6., 9., 0., 0., 0.],
    92598: [0., 2., 3., 0., 9., 8., 9., 9., 2., 0., 1.],
    93291: [2., 0., 5., 6., 8., 8., 9., 7., 4., 0., 1.],
    95684: [0., 2., 9., 7., 8., 9., 9., 6., 3., 0., 3.]
}

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
    if len(sequence) < 2:
        return False
    ratio = sequence[1] / sequence[0] if sequence[0] != 0 else 0
    for i in range(1, len(sequence)):
        if sequence[i - 1] == 0 or sequence[i] / sequence[i - 1] != ratio:
            return False
    return True

# Function to check if a sequence is a power series
def is_power_series(sequence):
    if len(sequence) < 2:
        return False
    base = sequence[1] / sequence[0] if sequence[0] != 0 else 0
    for i in range(1, len(sequence)):
        if sequence[i] != sequence[0] * (base ** i):
            return False
    return True

# Function to find sequences that follow a geometric progression or power series
def find_series_patterns(sequences):
    geometric_progression_indices = []
    power_series_indices = []
    for index, sequence in sequences.items():
        cleaned_sequence = preprocess_sequence(sequence)
        if is_geometric_progression(cleaned_sequence):
            geometric_progression_indices.append(index)
        if is_power_series(cleaned_sequence):
            power_series_indices.append(index)
    return geometric_progression_indices, power_series_indices

# Find sequences that follow a geometric progression or power series
geometric_progression_indices, power_series_indices = find_series_patterns(sequences)

# Print the results
print("Geometric progression indices:", geometric_progression_indices)
print("Power series indices:", power_series_indices)