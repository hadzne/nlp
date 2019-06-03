import re
import sys
from pathlib import Path
from collections import Counter
import argparse
from string import punctuation 
import math


def clean_up(doc):
    doc = doc.lower()
    doc = re.sub(r'[^a-zA-Z0-9\s]', ' ', doc)
    # add punctuation replace
    doc = re.sub('\n', ' ', doc)
    doc = re.sub('\t', ' ', doc)
    return doc


def prepare_dict(doc, n, show=False):
    doc = clean_up(doc)
    doc = ngrams(doc, n)
    doc = Counter(doc)
    if show:
        print("pokaz wykresy")
    doc = dict(doc)
    return doc


def ngrams(doc, n):
    tokens = [token for token in doc.split(" ") if token != ""]
    sequences = [tokens[i:] for i in range(1)]
    ngrams = zip(*sequences)
    value = [" ".join(ngram) for ngram in ngrams]
    return value