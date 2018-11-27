'''
    https://medium.com/@aneesha/using-tsne-to-plot-a-subset-of-similar-words-from-word2vec-bb8eeaea6229

    https://textminingonline.com/exploiting-wikipedia-word-similarity-by-word2vec

    https://textminingonline.com/dive-into-nltk-part-x-play-with-word2vec-models-based-on-nltk-corpus
    
    https://mubaris.com/posts/word2vec/
'''

# Word2Vec Model
from gensim.models import Word2Vec

# NLTK
import nltk
# nltk.download("gutenberg")

# Converting the corpus in to sentences
sentences = nltk.corpus.gutenberg.sents("carroll-alice.txt")

# Creating the model
model = Word2Vec(sentences, size=150, min_count=4, window=5, workers=4, sg=1)

# Vocabulary
words = list(model.wv.vocab)

# Vector of Alice
alice = model.wv["Alice"]
# print alice 

# Saving the model
model.save("alice.bin")

# Loading the saved model
model = Word2Vec.load("alice.bin")

# Similarity between 2 words
print model.wv.similarity("Alice", "Rabbit")
print model.wv.similarity("That", "baby")

# Similar Words
print model.wv.most_similar(positive=["Alice", "cat"], negative=["baby"]) 