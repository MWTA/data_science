"""
    Description: Compute sentence similarity using Wordnet
    Date: 13/11/2018
    Tutorial: https://nlpforhackers.io/wordnet-sentence-similarity/
"""

import gzip
import logging
from nltk.corpus import wordnet as wn

logging.basicConfig(format='% (asctime)s: % (levelname)s: % (message)s', level=logging.INFO)

input_file = '/home/rodriguesfas/Mestrado/workspace/similarity/category.txt'

"""with gzip.open(input_file, 'rb') as file:
    for i, line in enumerate(file):
        print(line)
        break"""