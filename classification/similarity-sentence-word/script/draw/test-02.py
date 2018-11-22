from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt

def closure_graph(synset, fn):
    seen = set()
    graph = nx.DiGraph()

    def recurse(s):
        if not s in seen:
            seen.add(s)
            graph.add_node(s.name())
            for s1 in fn(s):
                graph.add_node(s1.name())
                graph.add_edge(s.name(), s1.name())
                recurse(s1)

    recurse(synset)
    return graph


list_categories = [
    "actions", "alphabet", "animals", "body_parts", "clothing", 
    "color", "descriptors", "events", "expressions", "feelings",
    "food", "furniture", "games", "toys", "health", "materials", 
    "nature", "number", "objects", "people", "places", "quantity",
    "time", "sequence", "transports" ]

path_root = '/home/rodriguesfas/Mestrado/workspace/data_science/classification/similarity-sentence-word/dict/img'

for category in list_categories:
    sunset_word = wn.synsets(category)[0]
    
    G = closure_graph(sunset_word, lambda s: s.hypernyms())
    index = nx.betweenness_centrality(G)
    node_size = [index[n]*1000 for n in G]
    pos = nx.spring_layout(G)
    
    nx.draw_networkx(G, pos, node_size=node_size, edge_color='r', alpha=.9, linewidths=0)
    #plt.savefig(path_root + '/' + category + '.png')
    plt.show()