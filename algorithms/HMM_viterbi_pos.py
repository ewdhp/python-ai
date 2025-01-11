import numpy as np

# Define the HMM components
states = ['N', 'V', 'D', 'P']  # Noun, Verb, Determiner, Preposition
observations = ['time', 'flies', 'like', 'an', 'arrow']
start_prob = {'N': 0.4, 'V': 0.3, 'D': 0.2, 'P': 0.1}

# Transition probabilities (state to state)
trans_prob = {
    'N': {'N': 0.1, 'V': 0.4, 'D': 0.2, 'P': 0.3},
    'V': {'N': 0.3, 'V': 0.1, 'D': 0.4, 'P': 0.2},
    'D': {'N': 0.5, 'V': 0.2, 'D': 0.1, 'P': 0.2},
    'P': {'N': 0.6, 'V': 0.1, 'D': 0.1, 'P': 0.2},
}

# Emission probabilities (state to observation)
emission_prob = {
    'N': {'time': 0.3, 'flies': 0.1, 'like': 0.1, 'an': 0.05, 'arrow': 0.25},
    'V': {'time': 0.1, 'flies': 0.4, 'like': 0.3, 'an': 0.05, 'arrow': 0.15},
    'D': {'time': 0.05, 'flies': 0.05, 'like': 0.1, 'an': 0.7, 'arrow': 0.1},
    'P': {'time': 0.05, 'flies': 0.05, 'like': 0.6, 'an': 0.1, 'arrow': 0.2},
}

# Viterbi algorithm implementation
def viterbi(obs, states, start_prob, trans_prob, emission_prob):
    T = len(obs)
    n_states = len(states)

    # Initialize DP table and backpointer table
    dp = np.zeros((n_states, T))
    backpointer = np.zeros((n_states, T), dtype=int)

    # Map states to indices
    state_index = {state: i for i, state in enumerate(states)}

    # Initialization step
    for s in states:
        dp[state_index[s], 0] = start_prob[s] * emission_prob[s].get(obs[0], 0)

    # Recursion step
    for t in range(1, T):
        for s in states:
            max_prob, max_state = max(
                (dp[state_index[prev_s], t - 1] * trans_prob[prev_s][s] * emission_prob[s].get(obs[t], 0), prev_s)
                for prev_s in states
            )
            dp[state_index[s], t] = max_prob
            backpointer[state_index[s], t] = state_index[max_state]

    # Termination step
    last_state = np.argmax(dp[:, T - 1])
    best_path_prob = dp[last_state, T - 1]

    # Backtrack to find the best path
    best_path = []
    current_state = last_state
    for t in reversed(range(T)):
        best_path.insert(0, states[current_state])
        current_state = backpointer[current_state, t]

    return best_path, best_path_prob

# Run the Viterbi algorithm
best_path, best_prob = viterbi(observations, states, start_prob, trans_prob, emission_prob)

print("Best POS sequence:", best_path)
print("Probability of the best sequence:", best_prob)
