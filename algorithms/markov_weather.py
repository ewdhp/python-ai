import numpy as np

# Define states
states = ["Sunny", "Cloudy", "Rainy"]

# Initialize transition matrix
transition_matrix = np.array([
    [0.6, 0.3, 0.1],
    [0.2, 0.5, 0.3],
    [0.1, 0.2, 0.7]
])

# Choose the initial state
initial_state = 0  # Sunny

# Simulate the transitions
def simulate_weather(days, initial_state):
    state = initial_state
    weather_sequence = [states[state]]

    for _ in range(days - 1):
        state = np.random.choice([0, 1, 2], p=transition_matrix[state])
        weather_sequence.append(states[state])

    return weather_sequence

# Simulate for 10 days
weather_forecast = simulate_weather(10, initial_state)

# Display the results
print("10-Day Weather Forecast:")
print(weather_forecast)
