#%%
import numpy as np
from pathlib import Path
import time
import re
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
def levenshtein(s1, s2):
    l1 = len(s1) + 1
    l2 = len(s2) + 1
    m = np.zeros((l1, l2))
    for a in range(l1):
        m[a, 0] = a
    for b in range(l2):
        m[0,b] = b
    for a in range(1, l1):
        for b in range(1, l2):
            if s1[a-1]== s2[b-1]:
                m[a,b] = min(m[a-1, b] + 1, m[a-1, b-1], m[a, b-1]+1)
            else:
                m[a,b] = min(m[a-1, b] + 1, m[a-1, b-1]+1, m[a, b-1]+1)
    return int(m[l1-1, l2-1])

#%%
def pcw(c, w_dict):
    word_count = sum(w_dict.values())
    print("word_count" + str(word_count))
    max_prob = 0
    max_word = ''

    for k,v in w_dict.items():
        
        
        pc = (v **(1. / 10))/word_count
        pwc = 1 - (levenshtein(c, k) /max(len(k), len(c)))
        pcw = pwc * pc
        if pcw > max_prob:
            max_prob = pcw
            max_word = k
            print(k)
            print(v)
            print(pwc)
            print(pc)
            print("\n")
    return max_prob, max_word

#%%
f_formy = open(Path.cwd() / 'formy.txt', 'r', encoding='utf-8')
formy = f_formy.read()
f_formy.close()

f_publ = open(Path.cwd() / 'publ.txt', 'r', encoding='utf-8')
publ = f_publ.read()
f_publ.close()

f_bledy = open(Path.cwd() / 'bledy.txt', 'r', encoding='utf-8')
bledy = f_bledy.read()
f_bledy.close()



#%%

publ_dict = prepare_dict(publ, 1)
#%%

bledy = bledy.split("\n")

#%%
i = 0
for blad in bledy:
    good, bad = blad.split(";")
    if pcw(bad, publ) == good:
        i += 1
print(i/len(bledy))
#%%


print(pcw("dryektor", publ_dict))

#%%
a = "dryektor"
b = "dyrektor"
print(1- (levenshtein(a, b)/max(len(a), len(b)) ) )

#%%
print(publ_dict['do'])

#%%
