"""
The current implementation in your code is a basic Recurrent Neural Network (RNN) 
with a single hidden layer using the tanh activation function. This type of RNN 
is often referred to as a "Vanilla RNN" or "Simple RNN."


Key Characteristics of the Current Implementation:

- Single Hidden Layer: The RNN has one hidden layer.
- Tanh Activation Function: The tanh function is used as the activation function 
for the hidden layer.
- Backpropagation Through Time (BPTT): The gradients are calculated using BPTT.
- Gradient Clipping: Gradients are clipped to prevent exploding gradients.


Summary:

Name: Vanilla RNN or Simple RNN
Activation Function: Tanh
Training Method: Backpropagation Through Time (BPTT)
Gradient Handling: Gradient Clipping
This type of RNN is suitable for learning short-term dependencies in sequences 
but may struggle with long-term dependencies due to issues like vanishing and 
exploding gradients. For more complex tasks, architectures like Long Short-Term 
Memory (LSTM) or Gated Recurrent Unit (GRU) are often used.
"""
import numpy as np

# Tokenize the text into words
def tokenize(text):
    return text.split()

# Forward pass through the RNN over multiple time steps
def forward_pass(x_seq, h_prev):
    h_states = []  # To store hidden states
    y_hat_seq = []  # To store outputs
    h_current = h_prev

    for x in x_seq:
        h_current = np.tanh(np.dot(Wxh, x) + np.dot(Whh, h_current) + bh)
        y_hat = np.dot(Why, h_current) + by

        y_hat_seq.append(y_hat)
        h_states.append(h_current)

    return y_hat_seq, h_states

# Loss calculation using Mean Squared Error (MSE)
def calculate_loss(y_hat_seq, y_true_seq):
    loss = np.mean([np.mean((y_hat - y_true) ** 2) for y_hat, y_true in zip(y_hat_seq, y_true_seq)])
    return loss

# BPTT implementation
def bptt(x_seq, y_true_seq, h_states, y_hat_seq):
    dWxh, dWhh, dWhy = np.zeros_like(Wxh), np.zeros_like(Whh), np.zeros_like(Why)
    dbh, dby = np.zeros_like(bh), np.zeros_like(by)
    dh_next = np.zeros_like(h_states[0])
    
    for t in reversed(range(len(x_seq))):
        dy = (y_hat_seq[t] - y_true_seq[t])  # dL/dy
        dWhy += np.dot(dy, h_states[t].T)
        
        dby += np.sum(dy, axis=1, keepdims=True)
        dh = np.dot(Why.T, dy) + dh_next  # Backprop into h

        dhraw = (1 - h_states[t] ** 2) * dh  # backprop through tanh non-linearity
        dbh += np.sum(dhraw, axis=1, keepdims=True)
        dWxh += np.dot(dhraw, x_seq[t].T)
        if t != 0:
            dWhh += np.dot(dhraw, h_states[t-1].T)
        dh_next = np.dot(Whh.T, dhraw)

    return dWxh, dWhh, dWhy, dbh, dby

# Gradient clipping
def clip_gradients(gradients, max_value):
    for grad in gradients:
        np.clip(grad, -max_value, max_value, out=grad)

# SGD update
def sgd_update(params, grad_params, learning_rate):
    for param, grad in zip(params, grad_params):
        param -= learning_rate * grad

# Function to predict the next n words given an initial input
def predict_next_n_words(input_sequence, n):
    h_prev = np.zeros((hidden_size, 1))
    predicted_sequence = input_sequence
    
    for word in input_sequence:
        x = np.zeros((vocab_size, 1))
        x[word_to_ix[word]] = 1
        y_hat, h_prev = forward_pass_single(x, h_prev)
    
    for _ in range(n):
        x = np.zeros((vocab_size, 1))
        x[word_to_ix[predicted_sequence[-1]]] = 1
        y_hat, h_prev = forward_pass_single(x, h_prev)
        next_word = ix_to_word[np.argmax(y_hat)]
        predicted_sequence.append(next_word)
    
    return predicted_sequence

# Forward pass for a single time step
def forward_pass_single(x, h_prev):
    h_next = np.tanh(np.dot(Wxh, x) + np.dot(Whh, h_prev) + bh)
    y_hat = np.dot(Why, h_next) + by
    y_hat = np.exp(y_hat) / np.sum(np.exp(y_hat))
    return y_hat, h_next

# Function to create training data using sliding window approach
def create_training_data(text, window_size):
    X_train = []
    Y_train = []
    for i in range(len(text) - window_size):
        input_seq = text[i:i + window_size]
        target_seq = text[i + 1:i + window_size + 1]
        X_train.append([word_to_ix[word] for word in input_seq])
        Y_train.append([word_to_ix[word] for word in target_seq])
    return X_train, Y_train

# Convert sequences to one-hot encoded vectors
def one_hot_encode(sequences, vocab_size):
    one_hot_encoded = []
    for seq in sequences:
        one_hot_seq = np.zeros((vocab_size, len(seq)))
        for i, word_idx in enumerate(seq):
            one_hot_seq[word_idx, i] = 1
        one_hot_encoded.append(one_hot_seq)
    return one_hot_encoded

# Vowel sequence expanded with a clear pattern
sentences = [
    "when you do your homework", 
    "everything is fine", 
    "which are the best books to read?",  
    "how are you doing", 
    "the desert is hot",
    "we do what we do",
    "do you know what to do",
    "you do what you do",
    "i do what i do",
    "we do what we do best"
]

# Test the model by predicting a sequence of words starting from 'which are'
strn_sentence = "when you"
strn = tokenize(strn_sentence)
n = 10

# Tokenize the text into words
data = ' '.join(sentences)
words = tokenize(data)
unique_words = set(words)
vocab_size = len(unique_words)

# Create a mapping from word to index and vice versa
word_to_ix = {word: i for i, word in enumerate(unique_words)}
ix_to_word = {i: word for i, word in enumerate(unique_words)}

# Number of input, hidden, and output nodes
input_size = vocab_size
hidden_size = 200  # Increased hidden size
output_size = vocab_size

# Initialization of weights
Wxh = np.random.randn(hidden_size, input_size) * 0.01
Whh = np.random.randn(hidden_size, hidden_size) * 0.01
Why = np.random.randn(output_size, hidden_size) * 0.01

# Initialization of biases
bh = np.zeros((hidden_size, 1))
by = np.zeros((output_size, 1))

# Hyperparameters
learning_rate = 0.005  # Learning rate
num_epochs = 100
window_size = 40  # Increased sliding window size
max_grad_value = 1  # Gradient clipping threshold

# Prepare training data using sliding window approach
X_train, Y_train = create_training_data(words, window_size)

# Convert training data to one-hot encoded vectors
X_train = one_hot_encode(X_train, vocab_size)
Y_train = one_hot_encode(Y_train, vocab_size)

# Training loop
for epoch in range(num_epochs):
    h_prev = np.zeros((hidden_size, 1))  # Initial hidden state
    
    # Forward pass
    y_hat_seq, h_states = forward_pass(X_train, h_prev)
    
    # Loss calculation
    loss = calculate_loss(y_hat_seq, Y_train)
    
    # Backward pass (BPTT)
    dWxh, dWhh, dWhy, dbh, dby = bptt(X_train, Y_train, h_states, y_hat_seq)

    # Gradient clipping
    clip_gradients([dWxh, dWhh, dWhy, dbh, dby], max_grad_value)

    # SGD update
    params = [Why, Whh, Wxh, by, bh]
    grad_params = [dWhy, dWhh, dWxh, dby, dbh]
    sgd_update(params, grad_params, learning_rate)

    if epoch % 100 == 0:
        print(f'Epoch {epoch + 1}, Loss: {loss:.4f}, Gradients: dWxh: {np.linalg.norm(dWxh):.4f}, dWhh: {np.linalg.norm(dWhh):.4f}, dWhy: {np.linalg.norm(dWhy):.4f}, dbh: {np.linalg.norm(dbh):.4f}, dby: {np.linalg.norm(dby):.4f}')

# Print the final epoch's loss and gradients
print(f'Epoch {num_epochs}, Loss: {loss:.4f}, Gradients: dWxh: {np.linalg.norm(dWxh):.4f}, dWhh: {np.linalg.norm(dWhh):.4f}, dWhy: {np.linalg.norm(dWhy):.4f}, dbh: {np.linalg.norm(dbh):.4f}, dby: {np.linalg.norm(dby):.4f}')

predicted_sequence = predict_next_n_words(strn, n)
print(f'Predicted sequence: {" ".join(predicted_sequence)}')