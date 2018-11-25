'''
'''

from gensim.models import Word2Vec

model = Word2Vec.load('path/to/your/model')

model.similarity('france', 'spain')