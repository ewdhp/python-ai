import numpy as np

# Tokenize the text into words
def tokenize(text):
    return text.split()

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

# Tokenize the text into words
data = ' '.join(sentences)
words = tokenize(data)
unique_words = set(words)
vocab_size = len(unique_words)

# Create a mapping from word to index and vice versa
word_to_ix = {word: i for i, word in enumerate(unique_words)}
ix_to_word = {i: word for i, word in enumerate(unique_words)}

# Initialize the transition matrix
transition_matrix = np.zeros((vocab_size, vocab_size))

# Populate the transition matrix
for i in range(len(words) - 1):
    current_word = words[i]
    next_word = words[i + 1]
    transition_matrix[word_to_ix[current_word], word_to_ix[next_word]] += 1

# Normalize the counts to get probabilities
transition_matrix = transition_matrix / transition_matrix.sum(axis=1, keepdims=True)

# Function to predict the next word given the current word
def predict_next_word(current_word):
    current_word_idx = word_to_ix[current_word]
    next_word_idx = np.argmax(transition_matrix[current_word_idx])
    return ix_to_word[next_word_idx]

# Example usage
current_word = "when"
next_word = predict_next_word(current_word)
print(f'The next word after "{current_word}" is "{next_word}".')