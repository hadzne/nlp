#%%
from pathlib import Path

import preprocessing as prep
import language_detector as ld
import matplotlib.pyplot as plt
import pandas as pd
import time
import numpy as np



#%%

input_path = Path.cwd() / 'input'

n = 1
sentence = "hitler hat eine katze aber ich habe eine hund mit kartofeln"

f_en1 = open(input_path / 'english2.txt', 'r')
doc_en = f_en1.read()
f_en1.close()

f_en2 = open(input_path / 'english2.txt', 'r')
en2 = f_en2.read()
f_en2.close()

f_de = open(input_path / 'german1.txt', 'r')
doc_de = f_de.read()
f_de.close()


f_fi = open(input_path / 'finnish1.txt', 'r')
doc_fi = f_fi.read()
f_fi.close()

en2_tab = en2.split(".")

#%%
en2_tab = en2_tab[:1000]


#%%
doc_en = prep.prepare_dict(doc_en, n)
doc_de = prep.prepare_dict(doc_de, n)
doc_fi = prep.prepare_dict(doc_fi, n)
#%%

en_cnt = 0
de_cnt = 0
fi_cnt = 0

for i in range(len(en2_tab)):
    en2_tab[i] = prep.prepare_dict(str(en2_tab[i]),n)
    dist_en = ld.distance_cosinus(doc_en, en2_tab[i])
    dist_de = ld.distance_cosinus(doc_de, en2_tab[i])
    dist_fi = ld.distance_cosinus(doc_fi, en2_tab[i])
    max_dist = max(dist_en, dist_de, dist_fi)
    if max_dist == 0:
        pass
    elif max_dist == dist_de:
        de_cnt += 1
    elif max_dist == dist_de:
        fi_cnt += 1
    else:
        en_cnt += 1

print(de_cnt)
print(fi_cnt)
print(en_cnt)

sent_cnt = len(en2_tab)
tp = en_cnt/sent_cnt
tn = sent_cnt - de_cnt - fi_cnt - en_cnt
fp = de_cnt + fi_cnt
#%%

sorted_sent = sorted(doc_fi.items(), key=lambda x: x[1], reverse=True )

#%%

i = 20
df_sent = pd.DataFrame(sorted_sent)
print(df_sent)
plt.plot(df_sent.head(i)[0], df_sent.head(i)[1])
plt.xticks(rotation='vertical')



#%%
print(row[0] for row in sorted_sent)
print(row[1] for row in sorted_sent)

#%%

print(doc_en)

print(doc_de)

#%%
print(ld.distance_cosinus(doc_en, sentence))
print(ld.distance_cosinus(doc_de, sentence))
print(ld.distance_cosinus(doc_en, dict()))