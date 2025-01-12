# filepath: pos_following_word.py
import spacy
from collections import Counter

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Example text corpus
text = """
The quick brown fox jumps
"""

# Process the text with spaCy
doc = nlp(text)

# Specify the word or phrase to analyze
target_word = "fox"

# Find the POS tags following the target word
pos_tags_following = []

for i, token in enumerate(doc[:-1]):  # Exclude the last token to avoid index out of range
    if token.text.lower() == target_word.lower():
        next_token = doc[i + 1]
        pos_tags_following.append(next_token.pos_)

# Count the most common POS tags
pos_counts = Counter(pos_tags_following)

# Print the results
print(f"Most common POS tags following the word '{target_word}':")
for pos, count in pos_counts.most_common():
    print(f"{pos}: {count}")