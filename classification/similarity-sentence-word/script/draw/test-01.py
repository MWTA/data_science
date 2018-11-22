'''
    Tutorial: http://intelligentonlinetools.com/blog/2016/09/05/getting-wordnet-information-and-building-and-building-graph-with-python-and-networkx/
'''

from nltk.corpus import wordnet as wn

synonyms = []
antonyms = []

for syn in wn.synsets("good"):
    for l in syn.lemmas():
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())

print(set(synonyms))
print(set(antonyms))
print (syn.lemmas())


w1 = wn.synset('ship.n.01')
w2 = wn.synset('cat.n.01')
print(w1.wup_similarity(w2))

from textblob import Word
word = Word("plant")
print (word.synsets[:5])
print (word.definitions[:5])

word = Word("computer")
for syn in word.synsets:
    for l in syn.lemma_names():
        synonyms.append(l)
        
import networkx as nx
import matplotlib.pyplot as plt
G=nx.Graph()


w=word.synsets[1]


G.add_node(w.name())
for h in w.hypernyms():
      print (h)
      G.add_node(h.name())
      G.add_edge(w.name(),h.name())


for h in w.hyponyms():
      print (h)
      G.add_node(h.name())
      G.add_edge(w.name(),h.name())

print (G.nodes(data=True))
plt.show()
nx.draw(G, width=2, with_labels=True)
plt.savefig("path.png")