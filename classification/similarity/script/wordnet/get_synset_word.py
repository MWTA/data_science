# -*- coding: utf-8 -*-


from nltk.corpus import wordnet as wn

word = 'car'

synset = wn.synsets(word)
print synset
print synset[0].hypernym_paths()
print synset[0].definition()

print wn.synset('vehicle.n.01').definition()
#print wn.synset('profession.n.02').examples()
