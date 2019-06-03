#%%
from pathlib import Path

import preprocessing as prep
import matplotlib.pyplot as plt
import pandas as pd
import time
import numpy as np
import re
import math
from collections import Counter



#%%
def clean_up(doc):
    doc = doc.lower()
    doc = re.sub(r'[^.a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9\s]', ' ', doc)

    doc = doc.replace("\n", " ")
    doc = doc.replace(".", " ")
    doc = doc.replace(",", " ")
    doc = doc.replace("\t", " ")
    return doc

# Document should be cleaned up first
def ngrams(doc, n):
    tokens = [token for token in doc.split(" ") if token != ""]
    print(len(tokens))
    sequences = [tokens[i:] for i in range(n)]
    ngrams = zip(*sequences)
    value = [" ".join(ngram) for ngram in ngrams]
    print(len(value))
    return value

def prepare_dict(doc, n):
    doc = clean_up(doc)
    print(len(doc))
    doc = ngrams(doc, n)
    print(len(doc))
    doc = Counter(doc)
    print(len(doc))
    doc = dict(doc)
    return doc

#%%
def find_principal_form(forms, word):
    for family in forms:
        if word in family:
            return family[0]
    return word

#%%

input_path = Path.cwd() / 'inputt'

f_odm = open(input_path / 'odm.txt', 'r', encoding = 'utf8')
odm = f_odm.read()
f_odm.close()

f_potop = open(input_path / 'potop.txt', 'r', encoding = 'utf8')
potop = f_potop.read()
f_potop.close()

#%%


forms_list = odm.split("\n")

#%%

max_len = 1
for i in range(len(forms_list)):
    forms_list[i] = forms_list[i].replace(" ", "")
    forms_list[i] = forms_list[i].lower()
    forms = forms_list[i].split(",")

    if len(forms) > max_len:
        max_len = len(forms )


#%%
forms = [x[:] for x in [[] * max_len] * len(forms_list)]

for i in range(len(forms_list)):
    forms[i] = forms_list[i].split(",")
    
print(forms[20])
#%%
start = time.time()
principal_word = find_principal_form(forms, "zamieszaniu")
print(time.time() - start)
print(principal_word)
#%%
print(principal_word)


#%%
potop_dict = prepare_dict(potop, 1)

#%%
not_found = []
found = []
start = time.time()
princip_dict = dict(potop_dict)
i = 0
for k, v in potop_dict.items():
    princip = find_principal_form(forms, k)
    if princip != k:
        try:
            princip_dict[princip] += v
            del princip_dict[k]
        except KeyError:
            princip_dict[princip] = v

end = time.time()
print(end - start)
#%%

# print(list(princip_dict.keys()))
for i in princip_dict:
    print(i, princip_dict[i])

for i in potop_dict:
    print(i, princip_dict[i])
#%%
import csv

my_dict = {"test": 1, "testing": 2}

with open('mycsvfile.csv', 'w', encoding='utf-8') as f:
    w = csv.DictWriter(f, princip_dict.keys())
    w.writeheader()
    w.writerow(princip_dict)







#%%
