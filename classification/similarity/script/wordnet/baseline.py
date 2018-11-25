"""
    http://www.randomhacks.net/2009/12/29/visualizing-wordnet-relationships-as-graphs/
"""

import networkx as nx
import matplotlib.pyplot as pl

from graphviz import Digraph
from nltk.corpus import wordnet as wn

u = Digraph('unix', filename='/home/rodriguesfas/Mestrado/workspace/data_science/view_data/graphviz/unix.gv')
u.attr(size='6,6')
u.node_attr.update(color='lightblue2', style='filled')

def closure_graph(synset, fn):

    labels = {}
    seen = set()
    graph = nx.DiGraph()

    def recurse(s):
        if not s in seen:
            seen.add(s)
            graph.add_node(s.name)
            labels[s.name] = s.name().split(".")[0]
            for s1 in fn(s):
                graph.add_node(s1.name)
                graph.add_edge(s.name, s1.name)
                recurse(s1)

    recurse(synset)
    return graph, labels


synset = wn.synset('dog.n.01')

graph, labels = closure_graph(synset, lambda s: s.hypernyms())

index = nx.betweenness_centrality(graph)
node_size = [index[n]*1000 for n in graph]

nx.draw_networkx(
    graph, arrows=True, labels=labels, node_size=node_size, node_color=range(len(graph)), 
    prog='dot', alpha=.9, linewidths=2
)

pl.axis('off') # turn of axis
pl.show()
