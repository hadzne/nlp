#%%
import re
import math
from collections import Counter


def clean_up(doc):
    print("Hello")
    doc = doc.lower()
    print(len(doc))
    doc = re.sub(r'[^.a-zA-Z0-9\s]', ' ', doc)
    print(len(doc))
    # add punctuation replace
    print(len(doc))
    doc = re.sub('\n', ' ', doc)
    print(len(doc))
    doc = re.sub('.', ' ', doc)
    print(len(doc))
    doc = re.sub(',', '', doc)
    print(len(doc))
    doc = re.sub('\t', ' ', doc)
    print(len(doc))
    return doc

# Document should be cleaned up first
def ngrams(doc, n):
    tokens = [token for token in doc.split(" ") if token != ""]
    sequences = [tokens[i:] for i in range(n)]
    ngrams = zip(*sequences)
    value = [" ".join(ngram) for ngram in ngrams]
    print(len(value))
    return value

def prepare_dict(doc, n, show=False):
    return 0
    doc = clean_up(doc)
    doc = ngrams(doc, n)
    doc = Counter(doc)
    if show:
        print("pokaz wykresy")
    doc = dict(doc)
    return doc

#%%
