# -*- coding: utf-8 -*-

'''
    Description:
        Generate a heat map of the similarity of words and categories.
        Gerar um mapa de calor da similaridade das palavras e categorias

    Tutorial: http://dlacombejr.github.io/programming/2015/09/28/visualizing-cifar-10-categories-with-wordnet-and-networkx.html
              http://www.graphviz.org/gallery/

    Graphviz: https://graphviz.readthedocs.io/en/stable/index.html
    
    Date 24/11/2018
'''

import logging
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

from graphviz import Digraph

from nltk.corpus import genesis
from nltk.corpus import wordnet_ic
from nltk.corpus import wordnet as wn

logging.basicConfig(
    filename='data.log',
    filemode='w',
    format='%(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
)

plotly.tools.set_credentials_file(username='rodriguesfas', api_key='8pbWwhm2biYm8ApskFCl')

brown_ic = wordnet_ic.ic('ic-brown.dat')
semcor_ic = wordnet_ic.ic('ic-semcor.dat')
genesis_ic = wn.ic(genesis, False, 0.0)

path_root = '/home/rodriguesfas/Mestrado/workspace/data_science/classification/similarity/'

list_categories = set()
list_words = set()

# Set the labels
# label source:https://en.wikipedia.org/wiki/Basketball_statistics
labels_categories = []
labels_words = []



def load_data(path):
    temp_list = []

    with open(path, 'rb') as file:
        for i, line in enumerate(file):
            temp_list.append(line.strip('\n'))

    return temp_list


def calculater_similarity(list_categories, list_words):

    # empty similarity matix
    N_x = len(list_words)  # lines
    N_y = len(list_categories)  # columns

    print 'lines [words]: {} columns [categories]: {}'.format(N_x, N_y)

    similarity_matrix = np.zeros((N_x, N_y))

    # initialize counters
    x_index = 0
    y_index = 0

    # loop over all pairwise comparisons
    for category in list_categories:
        for word in list_words:
            try:
                x_word = wn.synsets(word)[0]
                y_category = wn.synset(category)
                # print y_category, x_word
                
                if x_word and y_category:
                    # enter similarity value into the matrix.
                    ''' WordNet Path Similarity '''
                    # similarity_matrix[x_index,y_index] = x_word.path_similarity(y_category)
                    
                    ''' + Wu-Palmer Similarity '''
                    similarity_matrix[x_index,y_index] = x_word.wup_similarity(y_category)

                    ''' Leacock-Chodorow Similarity '''
                    #similarity_matrix[x_index,y_index] = x_word.lch_similarity(y_category)

                    ''' Resnik Similarity '''
                    # similarity_matrix[x_index,y_index] = x_word.res_similarity(y_category, brown_ic)

                    ''' Jiang-Conrath Similarity '''
                    # similarity_matrix[x_index,y_index] = x_word.jcn_similarity(y_category, brown_ic)

                    ''' Lin Similarity '''
                    # similarity_matrix[x_index,y_index] = x_word.lin_similarity(y_category, brown_ic)
                    
                    # iterate x counter
                    x_index += 1
            except Exception as err:
                print 'word: {} category: {} err: {}'.format(x_word, y_category, err) 

        # reinitialize x counter and iterate y counter
        x_index = 0
        y_index += 1

    return similarity_matrix


def heatmap_plotly(similarity_matrix, labels_categories, labels_words):
    """
        plotly graphics interactive.
        https://plot.ly/python/annotated_heatmap/
        https://plot.ly/python/heatmaps/
    """
    trace = go.Heatmap(
        z=similarity_matrix,
        x=labels_categories, 
        y=labels_words
        )

    data = [trace]
    py.iplot(data, colorscale='Viridis', filename='HeatMap - WordNet Path Similarity')



if __name__ == '__main__':

    # load list_categories
    for category in load_data(path_root+'in/categories_synset.csv'):
        list_categories.add(category)

    # load list words.
    for word in load_data(path_root+'in/list_words.csv'):
        list_words.add(word)

    # get labels.
    for category in list_categories:
        labels_categories.append(category)

    for words in list_words:
        labels_words.append(words)

    # heatmap
    heatmap_plotly(calculater_similarity(list_categories, list_words), labels_categories, labels_words)
