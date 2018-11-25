# -*- coding: utf-8 -*-

"""
    Definition:
        Read a list of categories, get all the tasting category synsets for more detailed information about them.
        Ler uma lista de categorias, pega todos so synsets de cata categoria para obter informações mais detalhada das mesmas.
    
    Date: 21/11/2018
    Author: RodriguesFAS
    Email: franciscosouzaacer@gmail.com 
"""

import logging

from nltk import pos_tag
from nltk.corpus import wordnet as wn


path_root = '/home/rodriguesfas/Mestrado/workspace/data_science/classification/similarity-sentence-word/'


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


def get_synsets(list_words):
    list_synsets = []

    for word in list_words:
        try:
            list_synsets.append(wn.synsets(word, penn_to_wn(word)))
        except Exception as err:
            logging.error("Exception occurred! Word: " + word, exc_info=True)

    return list_synsets


def save_prediction(data):
    
        for label in data:
            file.write(str(label)+'\n')


if __name__ == '__main__':
    raw_date = load_data(path_root+'in/categories.csv')
    
    with open(path_root+'out/info_category.csv', 'w') as file:
        for category_synsets in get_synsets(raw_date):
            file.write('==================================\n')
            for c in category_synsets:
                file.write(c.name() + '\n')
                file.write('alternative names (lemmas): "%s"' % '", "'.join(c.lemma_names()) + '\n')
                file.write('definition: "%s"' % c.definition() + '\n')
                if c.examples():
                    file.write('example usage: "%s"' % '", "'.join(c.examples()) + '\n')
                #file.write('hypernyms: "%s"' % '", "'.join(c.hypernyms()) + '\n')
                #file.write('hypernyms: "%s"' % c.hypernyms() + '\n')
                #file.write('hypernym_paths: "%s"' % '", "'.join(c.hypernym_paths()) + '\n')
                file.write('hypernym_paths: "%s"' % c.hypernym_paths() + '\n')
                #file.write('hyponyms: "%s"' % '", "'.join(c.hyponyms()) + '\n')
                file.write('hyponyms: "%s"' % c.hyponyms() + '\n')
                #file.write('instance_hypernyms: "%s"' % '", "'.join(c.instance_hypernyms()) + '\n')
                #file.write('instance_hypernyms: "%s"' % c.instance_hypernyms() + '\n')
                file.write('\n\n')
