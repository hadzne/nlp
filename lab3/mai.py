#%%
import numpy as np
#%%
def longest_common_substring(s1, s2):
   m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
   longest = 0
   for x in range(1, 1 + len(s1)):
       for y in range(1, 1 + len(s2)):
           if s1[x - 1] == s2[y - 1]:
               m[x][y] = m[x - 1][y - 1] + 1
               if m[x][y] > longest:
                   longest = m[x][y]
           else:
               m[x][y] = 0
   return longest

print(longest_common_substring("string", "train"))

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
print(levenshtein("trufk", "kupa"))
print(longest_common_substring("trele", "jabaele"))
#%%
