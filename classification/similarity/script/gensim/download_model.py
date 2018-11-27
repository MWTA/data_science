"""
    https://radimrehurek.com/gensim/downloader.html
"""

import gensim.downloader as api

#print api.info() # return dict with info about available models/datasets.
#print api.info("text8") # return dict with info about "text8" dataset.



# -------------------------------------------------------------------------



model = api.load("glove-twitter-25")  # load glove vectors
print model.most_similar("cat")  # show words that similar to word 'cat'



# -------------------------------------------------------------------------



from gensim.models import Word2Vec

dataset = api.load("text8")  # load dataset as iterable
model = Word2Vec(dataset)  # train w2v model



# -------------------------------------------------------------------------


