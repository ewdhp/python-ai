import time
import numpy as np
from itertools import permutations

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

def forward_pass_single(x, h_prev):
    h_next = np.tanh(np.dot(Wxh, x) + np.dot(Whh, h_prev) + bh)
    y_hat = np.dot(Why, h_next) + by
    y_hat = np.exp(y_hat) / np.sum(np.exp(y_hat))
    return y_hat, h_next
# Sample POS tagging for sentences (this should be replaced with a real POS tagger in production)
def pos_tagging(sentence):
    # This is a mock POS tagger for demonstration purposes
    pos_tags = {
        "I": "PRP", "love": "VB", "running": "VBG", "fast": "RB",  # Example of POS tags
        "She": "PRP", "enjoys": "VB", "reading": "VBG", "books": "NNS",
        "They": "PRP", "are": "VBP", "studying": "VBG", "hard": "RB"
    }
    return [pos_tags.get(word, "NN") for word in sentence.split()]

# Convert sequences to one-hot encoded matrices
def one_hot_encode(sequences, vocab_size):
    one_hot_encoded = []
    for seq in sequences:
        one_hot_seq = np.zeros((vocab_size, len(seq)))
        for i, word_idx in enumerate(seq):
            one_hot_seq[word_idx, i] = 1
        one_hot_encoded.append(one_hot_seq)
    return one_hot_encoded

# Convert POS tags to one-hot encoded matrices
def one_hot_encode_pos(tags, pos_vocab_size):
    one_hot_encoded = []
    for tag in tags:
        one_hot_tag = np.zeros((pos_vocab_size, 1))
        tag_idx = pos_tag_to_ix.get(tag, 0)  # default to index 0 if tag is unknown
        one_hot_tag[tag_idx, 0] = 1
        one_hot_encoded.append(one_hot_tag)
    return one_hot_encoded

start_time = time.time()

# Example sentences and their POS tags
sentences = [
    "I love running fast",
    "She enjoys reading books",
    "They are studying hard"
]

# Tokenize the text into words and generate POS tags
words = [tokenize(sentence) for sentence in sentences]
pos_tags = [pos_tagging(sentence) for sentence in sentences]

# Build vocabularies for words and POS tags
unique_words = set(word for sentence in words for word in sentence)
unique_pos_tags = set(tag for sentence in pos_tags for tag in sentence)

vocab_size = len(unique_words)
pos_vocab_size = len(unique_pos_tags)

# Create mappings from word and POS tag to index, and vice versa
word_to_ix = {word: i for i, word in enumerate(unique_words)}
ix_to_word = {i: word for i, word in enumerate(unique_words)}

pos_tag_to_ix = {tag: i for i, tag in enumerate(unique_pos_tags)}
ix_to_pos_tag = {i: tag for i, tag in enumerate(unique_pos_tags)}

# Number of input, hidden, and output nodes
hidden_size = 50  # Increased hidden size
output_size = vocab_size  # Predict next word (output_size is vocab_size)

# Initialization of weights
Wxh = np.random.randn(hidden_size, vocab_size + pos_vocab_size) * 0.01
Whh = np.random.randn(hidden_size, hidden_size) * 0.01
Why = np.random.randn(output_size, hidden_size) * 0.01

# Initialization of biases
bh = np.zeros((hidden_size, 1))
by = np.zeros((output_size, 1))

# Hyperparameters
learning_rate = 0.005
num_epochs = 50
window_size = 9
max_grad_value = 1

# Create the X and Y matrices directly from sentences
X_train = []
Y_train = []

# Generate X and Y with words and their corresponding POS tags
for sentence, pos_tag_sequence in zip(words, pos_tags):
    for i in range(len(sentence) - 1):  # Use all but the last word
        word = sentence[i]
        next_word = sentence[i + 1]
        pos_tag = pos_tag_sequence[i]
        next_pos_tag = pos_tag_sequence[i + 1]
        
        # Create the input (word + POS tag one-hot)
        x_word = word_to_ix[word]
        x_pos_tag = pos_tag_to_ix[pos_tag]
        x = np.concatenate((np.eye(vocab_size)[x_word], np.eye(pos_vocab_size)[x_pos_tag]), axis=0).reshape(-1, 1)
        
        # Create the output (next word one-hot)
        y_word = word_to_ix[next_word]
        y = np.eye(vocab_size)[y_word].reshape(-1, 1)
        
        # Append to the training data
        X_train.append(x)
        Y_train.append(y)

# Convert to numpy arrays for further processing
X_train = np.array(X_train)
Y_train = np.array(Y_train)

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
        print(f'Epoch {epoch + 1}, Loss: {loss:.4f}')

end_time = time.time()

print(f'Training time: {end_time - start_time:.2f} seconds')

# Print the final epoch's loss
print(f'Epoch {num_epochs}, Loss: {loss:.4f}')

# Print the POS-tagged words for each sentence
for sentence, pos_tag_sequence in zip(sentences, pos_tags):
    word_pos_tag_pairs = list(zip(sentence.split(), pos_tag_sequence))
    print("Sentence:", sentence)
    print("POS Tagged:", word_pos_tag_pairs)
    print()
