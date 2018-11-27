"""
    https://spacy.io/usage/vectors-similarity
"""

import spacy

nlp = spacy.load('en_core_web_sm')
tokens = nlp(u'dog cat banana')

for token_1 in tokens:
    for token_2 in tokens:
        print token_1.text, token_2.text, token_1.similarity(token_2)