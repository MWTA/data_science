# -*- coding: utf-8 -*-
"""
    Description: Compute sentence similarity using Wordnet
    Date: 13/11/2018
    Tutorial: https://nlpforhackers.io/wordnet-sentence-similarity/

    Metrics Calculater Similarity: http://www.nltk.org/howto/wordnet.html
              
    Outher: http://sematch.cluster.gsi.dit.upm.es/
            https://github.com/gsi-upm/sematch
"""

import logging

from nltk import pos_tag
from nltk.corpus import genesis
from nltk.corpus import wordnet_ic
from nltk.corpus import wordnet as wn

from sklearn.metrics import accuracy_score, precision_recall_fscore_support

logging.basicConfig(
    filename='data.log',
    filemode='w',
    format='%(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
    )



prediction = []

brown_ic = wordnet_ic.ic('ic-brown.dat')
semcor_ic = wordnet_ic.ic('ic-semcor.dat')
genesis_ic = wn.ic(genesis, False, 0.0)



def load_data(path):
    temp_list = []

    with open(path, 'rb') as file:
        for i, line in enumerate(file):
            temp_list.append(line.strip('\n'))

    return temp_list


def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'

    if tag.startswith('V'):
        return 'v'

    if tag.startswith('J'):
        return 'a'

    if tag.startswith('R'):
        return 'r'

    return None


def get_synsets(list_words, option):
    list_synsets = []

    for word in list_words:
        try:
            if option == 0:
                item = { "word": word, "synset_word": wn.synsets(word, penn_to_wn(word))[0]}
            if option == 1:
                item = { "category": word, "synset_category": wn.synsets(word, penn_to_wn(word))[0]}
            list_synsets.append(item)  # Get the most common synset
        except Exception as err:
            #prediction.append(str(word + ', ' + 'no_category'))
            prediction.append('no_category')
            logging.error("Exception occurred! Word: " + word, exc_info=True)

    return list_synsets


def save_prediction(data):
    with open(path_root+'out/words_classification.json', 'w') as file:
        for label in data:
            file.write(str(label)+'\n')



if __name__ == '__main__':

    # You can read more about the different types of wordnet similarity measures here: http://www.nltk.org/howto/wordnet.html
    path_root = '/home/rodriguesfas/Mestrado/workspace/data_science/classification/similarity-sentence-word/'

    list_words = load_data(path_root+'in/words.csv')
    list_categories = load_data(path_root+'in/categories.csv')
    list_label_true = load_data(path_root+'in/label.csv')

    for word_synset in get_synsets(list_words, 0):
        word_list_similarity = []
        
        for synset_category in get_synsets(list_categories, 1):
            
            ''' Wu-Palmer Similarity '''
            similarity = word_synset['synset_word'].wup_similarity(synset_category['synset_category'])
            
            ''' Leacock-Chodorow Similarity '''
            #similarity = word_synset['synset_word'].lch_similarity(synset_category['synset_category'])
            
            ''' PATH - Retorna uma pontuação indicando a similaridade entre duas palavras com base no caminho mais curto que coneca os sentido na taxonomia (hypernym/hypnoym) '''
            #similarity = word_synset['synset_word'].path_similarity(synset_category['synset_category'])

            ''' Resnik Similarity '''
            #similarity = word_synset['synset_word'].res_similarity(synset_category['synset_category'], brown_ic)

            ''' Jiang-Conrath Similarity '''
            # similarity = word_synset['synset_word'].jcn_similarity(synset_category['synset_category'], brown_ic)

            ''' Lin Similarity '''
            #similarity = word_synset['synset_word'].lin_similarity(synset_category['synset_category'], brown_ic)
            
            # print "Similarity(%s, %s) = %s" % (word_synset, synset, similarity)
            # print '\n Selected:', str(word_synset) + ', ' + str(synset_category) + ' = ' + str(similarity)
            
            item = {
                "synset_word": word_synset, 
                "synset_category": synset_category,
                "similarity": similarity,
            }
            
            word_list_similarity.append(item)

        
        # get result category max value similarity.
        selected = max(word_list_similarity, key=lambda item:item['similarity'])

        
        #prediction.append(selected['synset_category']['category'])
        prediction.append(str(selected['synset_word']['word'] + ', ' + selected['synset_category']['category'] ) )
        #prediction.append(str(selected) + '\n')

        # show
        #print '\n Selected:', selected['synset_word']['word'] + ', ' + selected['synset_category']['category']
    

    save_prediction(prediction)

    #print accuracy_score(list_label_true, prediction)
    #print accuracy_score(list_label_true, prediction, normalize=False)
    #print precision_recall_fscore_support(list_label_true, prediction, average='macro')