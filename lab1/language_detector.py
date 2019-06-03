import re
import sys
from pathlib import Path
from collections import Counter
import argparse
from string import punctuation 
import math

import preprocessing as prep


n = 1

# Document should be cleaned up first
def ngrams(doc, n):
    tokens = [token for token in doc.split(" ") if token != ""]
    sequences = [tokens[i:] for i in range(n)]
    ngrams = zip(*sequences)
    value = [" ".join(ngram) for ngram in ngrams]
    return value



# Gets dict
def norm_euclidian_vector(vector):
    denominator = [v**2 for k, v in vector.items()]
    denominator = math.sqrt(sum(denominator))

    vector = {k: v/denominator for k, v in vector.items()}
    # vector = [(k, v/denominator) for k, v in vector]
    return vector


# Binary approach
def distance_euclidian(language, sentence):
    deltas = 0
    for k, v in language.items():
        try:
            value_sentence = sentence[k]
        except KeyError:
            value_sentence = 0
        
        delta = (v - value_sentence)**2
        deltas += delta
    distance = math.sqrt(deltas)
    return distance

def distance_cosinus(language, sentence):
    lenght = len(language)

    added = 0
    for k, v in language.items():
        try:
            value_sentence = sentence[k]
        except KeyError:
            value_sentence = 0

        added += v * value_sentence
    distance = added/(lenght**2)
    return distance



def check_language_norm_euclides(language, sentence):
    # i = 0
    # i for i in language if i in sentence
    for ngram in sentence:
        if ngram in language:
            i += 1
    norm = math.sqrt(len(language)-i)
    return norm




# sentence = norm_euclidian_vector(sentence)
# doc_en = norm_euclidian_vector(doc_en)
# doc_de = norm_euclidian_vector(doc_de)

# dist_en = distance_euclidian(doc_en, sentence)
# dist_de = distance_euclidian(doc_de, sentence)

# print(dist_en)
# print(dist_de)