import random
from collections import defaultdict

# Example training data: posts with tags
training_data = [
    ("How to train a neural network", ["AI", "Machine Learning"]),
    ("Introduction to Python programming", ["Python", "Programming"]),
    ("Latest advancements in AI technology", ["AI", "Technology"]),
    ("How to write unit tests in Python", ["Python", "Testing"]),
    ("Understanding Markov chains", ["Mathematics", "AI"]),
]

# Step 1: Train the Markov chain
def train_markov_chain(training_data):
    chain = defaultdict(lambda: defaultdict(int))
    
    for _, tags in training_data:
        # Add start and end markers to the sequence
        tags = ["<START>"] + tags + ["<END>"]
        for i in range(len(tags) - 1):
            current_tag = tags[i]
            next_tag = tags[i + 1]
            chain[current_tag][next_tag] += 1
    
    # Normalize the probabilities
    for current_tag, transitions in chain.items():
        total = sum(transitions.values())
        chain[current_tag] = {tag: count / total for tag, count in transitions.items()}
    
    return chain

# Step 2: Generate tags for a new post
def generate_tags(chain, max_tags=5):
    current_tag = "<START>"
    tags = []
    
    while current_tag != "<END>" and len(tags) < max_tags:
        next_tag = random.choices(
            list(chain[current_tag].keys()),
            weights=chain[current_tag].values()
        )[0]
        if next_tag != "<END>":
            tags.append(next_tag)
        current_tag = next_tag
    
    return tags

# Train the Markov chain
markov_chain = train_markov_chain(training_data)

# Example: Tagging a new post
new_post = "How to program in Python and test your code"
print("Post:", new_post)
predicted_tags = generate_tags(markov_chain)
print("Predicted Tags:", predicted_tags)
