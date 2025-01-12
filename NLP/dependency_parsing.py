import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Example sentence
sentence = "The quick brown fox jumps over the lazy dog."

# Process the sentence with spaCy
doc = nlp(sentence)

# Extract features for each token in the sentence
for token in doc:
    features = {
        "word_form": token.text,
        "pos_tag": token.pos_,
        "lemma": token.lemma_,
        "word_shape": token.shape_,
        "dependency_relation": token.dep_,
        "head_word": token.head.text,
        "distance_to_head": abs(token.i - token.head.i),
        "sibling_relations": [child.dep_ for child in token.head.children if child != token],
        "word_position": token.i,
        "previous_word": doc[token.i - 1].text if token.i > 0 else None,
        "next_word": doc[token.i + 1].text if token.i < len(doc) - 1 else None,
        "prefix": token.text[:3],
        "suffix": token.text[-3:],
        "case": "uppercase" if token.is_upper else "lowercase" if token.is_lower else "titlecase" if token.is_title else "mixed",
        "subcategorization": token.head.pos_,
        "word_clusters": token.vector,
        "ner": token.ent_type_,
        "dependency_tree_depth": len(list(token.ancestors)),
        "head_pos_tag": token.head.pos_,
        "sentence_length": len(doc),
        "relative_position": "before" if token.i < token.head.i else "after",
        "punctuation": token.is_punct,
        "prev_head": doc[token.i - 1].head.text if token.i > 0 else None,
        "next_head": doc[token.i + 1].head.text if token.i < len(doc) - 1 else None,
        "sentence_punctuation": [tok.text for tok in doc if tok.is_punct],
    }
    print(features)