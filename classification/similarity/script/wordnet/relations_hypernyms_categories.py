# -*- coding: utf-8 -*-

'''
    Description: Generates graph heat map and hierarchical similarity of categories.
                 Gera gráfico mapa de calor e de hierárquico da similaridade das categorias

    Tutorial: http://dlacombejr.github.io/programming/2015/09/28/visualizing-cifar-10-categories-with-wordnet-and-networkx.html
              http://www.graphviz.org/gallery/

    Graphviz: https://graphviz.readthedocs.io/en/stable/index.html
    
    Date 24/11/2018
'''

import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

from graphviz import Digraph
from nltk.corpus import wordnet_ic
from nltk.corpus import wordnet as wn

import plotly
import plotly.plotly as py
import plotly.graph_objs as go



def load_data(path):
    temp_list = []
    with open(path, 'rb') as file:
        for i, line in enumerate(file):
            temp_list.append(line.strip('\n'))
    return temp_list


def wordnet_graph(words):

     seen = set()
     
     def recurse(word_synset):

         """ Recursively move up semantic hierarchy and add nodes / edges """  
 
         if not word_synset in seen:                           # if not seen...
             seen.add(word_synset)                             # add to seen
             hypernyms = word_synset.hypernyms()               # get hypernyms
 
             for s1 in hypernyms:                              # for hypernyms
                 recurse(s1)                                   # do so until top
                 dot.edge( str(word_synset.name()), str(s1.name()) )
      
     # build network containing all categories          
     for word in words:                                        # for all categories
         word_synset = wn.synset(word)                         # create synset            
         recurse(word_synset)                                  # call recurse

     dot.view()



def calculater_similarity():
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

    # convert the main diagonal of the matrix to zeros.
    similarity_matrix = similarity_matrix * abs(np.eye(len(categories)) - 1)

    return similarity_matrix



def heatmap_matplot():
    # Set the labels
    # label source:https://en.wikipedia.org/wiki/Basketball_statistics
    labels = []

    for category in categories:
        labels.append(category)

    # Plot it out
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(similarity_matrix, cmap='hot', alpha=0.9)

    # Format
    fig = plt.gcf()
    fig.set_size_inches(8, 11)

    # turn off the frame
    ax.set_frame_on(False)

    # put the major ticks at the middle of each cell
    ax.set_yticks(np.arange(similarity_matrix.shape[0]) + 0.5, minor=False)
    ax.set_xticks(np.arange(similarity_matrix.shape[1]) + 0.5, minor=False)

    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    # note I could have used nba_sort.columns but made "labels" instead
    ax.set_xticklabels(labels, minor=False)
    ax.set_yticklabels(labels, minor=False)

    # rotate the x-axis labels
    plt.xticks(rotation=90)
    
    ax.grid(False)

    # Turn off all the ticks
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')

    for t in ax.xaxis.get_major_ticks():
        t.tick1On = False
        t.tick2On = False

    for t in ax.yaxis.get_major_ticks():
        t.tick1On = False
        t.tick2On = False

    fig.tight_layout()
    plt.show()


def heatmap_plotly():
    # plotly graphics interactive.
    # https://plot.ly/python/annotated_heatmap/
    # https://plot.ly/python/heatmaps/
    trace = go.Heatmap(z=similarity_matrix, x=labels, y=labels)
    data = [trace]
    py.iplot(data, filename='labelled-heatmap')



if __name__ == '__main__':

    path_root = '/home/rodriguesfas/Mestrado/workspace/data_science/classification/similarity/'
    
    plotly.tools.set_credentials_file(username='rodriguesfas', api_key='8pbWwhm2biYm8ApskFCl')

    dot = Digraph('diagram', format='svg', filename=path_root+'out/img/relations/relations_hypernyms_categories.gv')
    dot.attr(size='6,6')
    dot.node_attr.update(color='lightblue2', style='filled')

    categories = set()
    words = set()

    for category in load_data(path_root+'in/categories_synset.csv'):
        categories.add(category)

    wordnet_graph(categories)
    similarity_matrix = calculater_similarity()