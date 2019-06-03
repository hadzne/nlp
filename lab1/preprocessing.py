import re
import math
from collections import Counter


def clean_up(doc):
    doc = doc.lower()
    doc = re.sub(r'[^.a-zA-Z0-9\s]', ' ', doc)
    # add punctuation replace
    doc = re.sub('\n', ' ', doc)
    doc = re.sub('\t', ' ', doc)
    return doc

# Document should be cleaned up first
def ngrams(doc, n):
    tokens = [token for token in doc.split(" ") if token != ""]
    sequences = [tokens[i:] for i in range(n)]
    ngrams = zip(*sequences)
    value = [" ".join(ngram) for ngram in ngrams]
    return value

def prepare_dict(doc, n, show=False):
    doc = clean_up(doc)
    doc = ngrams(doc, n)
    doc = Counter(doc)
    if show:
        print("pokaz wykresy")
    doc = dict(doc)
    return doc