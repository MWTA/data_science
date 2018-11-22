# -*- coding: utf-8 -*-

'''
    Tutorial: http://dlacombejr.github.io/programming/2015/09/28/visualizing-cifar-10-categories-with-wordnet-and-networkx.html
              http://www.graphviz.org/gallery/
    Date 22/11/2018
'''

#%%
import numpy as np
import networkx as nx
import matplotlib.pyplot as pl

from nltk.corpus import wordnet_ic
from nltk.corpus import wordnet as wn 
from networkx.drawing.nx_agraph import graphviz_layout

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='rodriguesfas', api_key='8pbWwhm2biYm8ApskFCl')


list_test = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

list_words = ['dog', 'cat', 'bird', 'horse']

list_categories = [
    'actions', 'alphabet', 'animals', 'body_parts', 'clothing', 'color', 'descriptors', 'events', 
    'expressions', 'feelings', 'food', 'furniture', 'games', 'toys', 'health', 'materials', 'nature',
    'number', 'objects', 'people', 'places', 'quantity', 'time', 'sequence', 'transports'
]

categories = set()

for word in list_words:
    categories.add(word)


def wordnet_graph(words):
     """
     Construct a semantic graph and labels for a set of object categories using 
     WordNet and NetworkX. 
     
     Parameters: 
     ----------
     words : set
         Set of words for all the categories. 
         
     Returns: 
     -------
     graph : graph
         Graph object containing edges and nodes for the network. 
     labels : dict
         Dictionary of all synset labels. 
     """
     
     graph = nx.Graph()
     labels = {}
     seen = set()
     
     def recurse(s):
         
         """ Recursively move up semantic hierarchy and add nodes / edges """  
 
         if not s in seen:                               # if not seen...
             seen.add(s)                                 # add to seen
             graph.add_node(s.name)                      # add node
             labels[s.name] = s.name().split(".")[0]
             #labels[s.name] = s.name()     # add label
             hypernyms = s.hypernyms()                   # get hypernyms
 
             for s1 in hypernyms:                        # for hypernyms
                 graph.add_node(s1.name)                 # add node
                 graph.add_edge(s.name, s1.name)         # add edge between
                 recurse(s1)                             # do so until top
      
     # build network containing all categories          
     for word in words:                                  # for all categories
         s = wn.synsets(word)[0]         # create synset            
         recurse(s)                                      # call recurse
     
     # return the graph and labels    
     return graph , labels



# create the graph and labels
graph, labels = wordnet_graph(categories)

index = nx.betweenness_centrality(graph)
node_size = [index[n]*1000 for n in graph]
pos = nx.spring_layout(graph)

# draw the graph
nx.draw_networkx(graph, pos=pos, labels=labels, node_size=node_size, edge_color='r', alpha=.9, linewidths=0)
pl.show()



# --------------------------------------------------------------------------
# empty similarity matix
N = len(categories)

similarity_matrix = np.zeros((N, N))

# initialize counters
x_index = 0
y_index = 0

# loop over all pairwise comparisons
for category_x in categories:
    for category_y in categories:
        x = wn.synsets(category_x)[0]
        y = wn.synsets(category_y)[0]
        
        # enter similarity value into the matrix
        similarity_matrix[x_index, y_index] = x.path_similarity(y) 
        
        # iterate x counter
        x_index += 1
    
    # reinitialize x counter and iterate y counter   
    x_index = 0
    y_index += 1

# convert the main diagonal of the matrix to zeros       
#similarity_matrix = similarity_matrix * abs(np.eye(len(categories)) - 1)

# Plot it out
fig, ax = pl.subplots()
heatmap = ax.pcolor(similarity_matrix, alpha=0.9)

# Format
fig = pl.gcf()
fig.set_size_inches(8, 11)

# turn off the frame
ax.set_frame_on(False)

# put the major ticks at the middle of each cell
ax.set_yticks(np.arange(similarity_matrix.shape[0]) + 0.5, minor=False)
ax.set_xticks(np.arange(similarity_matrix.shape[1]) + 0.5, minor=False)

# want a more natural, table-like display
ax.invert_yaxis()
ax.xaxis.tick_top()

# Set the labels

# label source:https://en.wikipedia.org/wiki/Basketball_statistics
labels = []
for category in categories:
    labels.append(category)
 

# note I could have used nba_sort.columns but made "labels" instead
ax.set_xticklabels(labels, minor=False)
ax.set_yticklabels(labels, minor=False)

# rotate the x-axis labels
pl.xticks(rotation=90)
 
ax.grid(False)

# Turn off all the ticks
ax = pl.gca()
ax.set_aspect('equal', adjustable='box')

for t in ax.xaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False
for t in ax.yaxis.get_major_ticks():
    t.tick1On = False
    t.tick2On = False

pl.show()



# --------------------------------------------------------------------------
# plot.ly graphics interactive.
trace = go.Heatmap(z=similarity_matrix, x=labels, y=labels)
data=[trace]
py.iplot(data, filename='labelled-heatmap')