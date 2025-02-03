"""
Key Ideas on Using N-th Matrices/Tensors for Modeling:
Word Features with Multiple Dimensions (e.g., N-th Tensors):

Each word in a sentence can have more than just one feature (e.g., embedding, part-of-speech (POS) tag, sentiment, etc.). To represent this, you can use an n-th tensor where:
The first dimension could represent words in a sequence.
The second dimension could represent different features (e.g., word embeddings, POS tags, etc.).
Additional dimensions could represent contextual information (e.g., time steps, attention mechanisms).
Text Representation with Multiple Views:

You can represent text (or any sequence) using a tensor where each word is encoded with multiple features, such as:
Word embeddings (semantic features).
POS tags (syntactic features).
Dependency relations (syntactic structure).
Sentiment or other attributes.
This allows you to model complex dependencies between these features and incorporate them into a more powerful model.
N-th Tensor Representation:

Let's say you want to represent a sequence of words with both semantic features and syntactic features. A tensor could represent these features as follows:
1st dimension: The sequence length (number of words in the sentence).
2nd dimension: The word embeddings.
3rd dimension: Additional features (e.g., POS tags, sentiment scores, etc.).
Higher dimensions could represent interactions, context, or temporal dynamics.
Multi-Modal Input:

If you're using multi-modal inputs (e.g., combining text with images or audio), you can stack different types of data in a tensor, which can then be processed by models that handle such complex, high-dimensional data. For instance:
1st dimension: Words in a sentence.
2nd dimension: Word embedding vectors.
3rd dimension: Additional features such as POS or sentiment labels.
4th dimension: Features related to another modality (e.g., visual features or audio signals).
Applications:

Text Classification: For a document classification task, you could have a tensor where each document’s features (word embeddings, syntactic features, etc.) are stacked in different dimensions.
Sequence Labeling (POS, NER): You can represent sequences in a tensor format to capture multi-dimensional word features (embedding, POS, etc.) and their relationships, making it easier for models like CRFs, BiLSTM, or Transformers to predict labels based on rich, multi-featured inputs.
Multi-Task Learning: You could use multi-dimensional tensors to model tasks where you want to predict multiple labels for each input (e.g., predict both POS tags and sentiment for each word in the sentence).
Example: N-th Matrix Representation for Text + POS + Sentiment
Let’s assume you want to represent a sentence with 3 features for each word:

Word embedding (dimension: 50).
POS tag (dimension: 5) (one-hot encoded or embeddings).
Sentiment score (dimension: 1) (e.g., a numeric value between -1 and 1).
You could represent this as a 3D tensor where:

1st dimension: Number of words (sequence length).
2nd dimension: Number of features (Word embedding + POS + Sentiment).
3rd dimension: The size of each feature vector (Word embedding size, POS vector size, sentiment size).
So, for a sentence like "The cat sleeps", you would have a tensor of shape (3, 56):

3 words in the sentence.
56 total features: 50 for word embedding, 5 for POS tags, and 1 for sentiment.
"""

import numpy as np

# Example features for each word
word_embeddings = np.random.rand(3, 50)  # 3 words, 50-dimensional embeddings
pos_embeddings = np.random.rand(3, 5)   # 3 words, 5-dimensional POS features
sentiment_scores = np.random.rand(3, 1)  # 3 words, 1-dimensional sentiment score

# Stack the features along the second axis to form a 3D tensor
sentence_features = np.concatenate([word_embeddings, pos_embeddings, sentiment_scores], axis=1)

print("Shape of the sentence features tensor:", sentence_features.shape)
print(sentence_features)
