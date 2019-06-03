import pickle
import re

from difflib import SequenceMatcher

from nltk import edit_distance
from sklearn.cluster import DBSCAN
from nltk.util import ngrams

import numpy as np
import progressbar


class InputUtils:
    clean_pattern = re.compile('[/!@#$,.():\-?";\n\']')
    multiple_whitespace = re.compile('[\s\t]+')

    def __init__(self, dictionary_path):
        # mapa int -> str, int oznacza identyfikator linii
        self.lines = dict()
        self.inverse_lines = dict()

        self._prepare_stop_words()
        self._prepare_input(dictionary_path)

    def _prepare_input(self, file_name):
        with open(file_name) as f:
            for i, line in enumerate(f.readlines()):
                clean_string = self.clear_line(line)
                self.lines[i] = clean_string
                self.inverse_lines[clean_string] = i

    def get_equal_lines_as_char_vector(self):
        tmp = []
        longest = -1
        for i in range(len(self.lines)):
            line = self.lines[i]
            if len(line) > longest:
                longest = len(line)
            ascii_line = [ord(x) for x in line]
            tmp.append(ascii_line)

        output = []
        for t in tmp:
            tt = np.concatenate([np.array(t), np.zeros(longest)])[:longest]
            output.append(tt)
        return output

    def get_lines_as_char_vector(self):
        output = []
        for i in range(len(self.lines)):
            line = self.lines[i]
            ascii_line = [ord(x) for x in line]
            output.append(ascii_line)
        return output

    def save_result(self, clusters, graph, file_name):
        result = self._classify_lines(clusters)

        davies_Bouldin_index = self.calculate_Davies_Bouldin_index(graph, result)
        dunn_index = self.calculate_Dunn_index(graph, result)

        with open(file_name, "w") as fp:
            for key, values in result.items():
                fp.write("############\n")
                print("############")
                for val in values:
                    fp.write("{}\n".format(val))
                    print(val)
                fp.write("\n")
                print()

            fp.write("\n")
            fp.write("davies_Bouldin_index: {}\n".format(davies_Bouldin_index))
            print("davies_Bouldin_index: {}".format(davies_Bouldin_index))
            fp.write("Dunn_index: {}\n".format(dunn_index))
            print("Dunn_index: {}".format(dunn_index))

    def calculate_Davies_Bouldin_index(self, graph, result):
        def index_options(centroids, result):
            for i in range(len(result)):
                for j in range(len(result)):
                    if i != j:
                        c = centroids[i] + centroids[j]
                        d = self.clusters_distance(result[i], result[j], graph)
                        if d != 0:
                            yield c / d

        centroids = []
        for key, value in result.items():
            centroids.append(self.cluster_centroid(graph, value))

        davies_Bouldin_index = max(index_options(centroids, result))
        return davies_Bouldin_index

    def calculate_Dunn_index(self, graph, result):
        def distance_options():
            for i in range(len(result)):
                for j in range(len(result)):
                    if i != j:
                        distance = self.clusters_distance(result[i], result[j], graph)
                        if distance > 0:
                            yield distance

        def cluster_size_options():
            for i in range(len(result)):
                yield self.cluster_size(result[i], graph)

        dunn_index = min(distance_options()) / max(cluster_size_options())
        return dunn_index


    def cluster_centroid(self, graph, value):
        def give_values():
            for v1 in value:
                for v2 in value:
                    pos1 = self.inverse_lines[v1]
                    pos2 = self.inverse_lines[v2]
                    if pos1 > pos2:
                        yield graph[pos1][pos2]

        res = [v for v in give_values()]
        # 1 bo odleglosci licze tylko do innych adresow w klastrze
        return sum(res) / (1 + len(res))

    def _classify_lines(self, clusters):
        result = dict()
        for i, c in enumerate(clusters):
            x = result.get(c, [])
            x.append(self.lines[i])
            result[c] = x
        return result

    def calculate_distance_matrix(self, metric, file_name):
        size = len(self.lines)
        result = [x[:] for x in [[0] * size] * size]

        m_v = 0.5 * size * size

        bar = progressbar.ProgressBar(maxval=int(m_v))
        c = 0
        for i in range(size):
            for j in range(i+1, size):
                result[i][j] = result[j][i] = metric(self.lines[i], self.lines[j])
                bar.update(c)
                c += 1
        bar.finish()

        with open(file_name, mode='wb') as binary_file:
            pickle.dump(result, binary_file)

    def calculate_distance_matrix_as_vector(self, metric, file_name):
        size = len(self.lines)
        result = [x[:] for x in [[0] * size] * size]
        # np.zeros(size, size)
        lines_vec = self.get_lines_as_char_vector()

        m_v = 0.5 * size * size

        bar = progressbar.ProgressBar(maxval=int(m_v))
        c = 0
        for i in range(size):
            for j in range(i+1, size):
                result[i][j] = result[j][i] = metric(lines_vec[i], lines_vec[j])
                bar.update(c)
                c += 1
        bar.finish()

        with open(file_name, mode='wb') as binary_file:
            pickle.dump(result, binary_file)

    def clear_line(self, line):
        line = re.sub(self.clean_pattern, ' ', line).lower()

        line = re.sub(self.multiple_whitespace, ' ', line).strip()
        line = ' '.join([w for w in line.split() if len(w) > 1 and w not in self.stop_words])
        return line

    def _prepare_stop_words(self):
        self.stop_words = []
        with open("data/stop_words.txt") as fp:
            for line in fp:
                self.stop_words.append(line.strip().lower())

    def clusters_distance(self, cluster1, cluster2, graph):
        def give_values():
            for v1 in cluster1:
                for v2 in cluster2:
                    pos1 = self.inverse_lines[v1]
                    pos2 = self.inverse_lines[v2]

                    yield graph[pos1][pos2]

        return max([v for v in give_values()])

    def cluster_size(self, cluster, graph):
        def give_values():
            for v1 in cluster:
                for v2 in cluster:
                    pos1 = self.inverse_lines[v1]
                    pos2 = self.inverse_lines[v2]

                    yield graph[pos1][pos2]

        return max([v for v in give_values()])


def levenshtein(seq1, seq2):
    # def clean_zeros(arr):
    #     return [int(x) for x in arr if x != 0]
    #
    # seq1 = clean_zeros(seq1)
    # seq2 = clean_zeros(seq2)

    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )
    return int(matrix[size_x - 1, size_y - 1])


def lcs_dist(a, b):
    # def clean_zeros(arr):
    #     return [int(x) for x in arr if x != 0]
    #
    # a = clean_zeros(a)
    # b = clean_zeros(b)
    try:
        s = SequenceMatcher(None, a, b)
        m = s.find_longest_match(0, len(a), 0, len(b))
        return 1 - m.size / max(len(a), len(b))
    except Exception:
        return 1


def levenstain(a, b):
    return edit_distance(a, b) / max(len(a), len(b))


def dice(a, b):
    tokens = [token for token in a.split(" ")]
    output1 = set(ngrams(tokens, 2))

    tokens = [token for token in b.split(" ")]
    output2 = set(ngrams(tokens, 2))

    if len(output1) + len(output2) == 0:
        return 1

    return 1 - 2 * len(output1 & output2) / (len(output1) + len(output2))


# print("levenstain.bin")
iu = InputUtils("data/lines.txt")
# iu.calculate_distance_matrix(dice, "dice.bin")


pickle_in = open("dice.bin", "rb")
my_graph = pickle.load(pickle_in)
#
dbscan = DBSCAN(eps=0.3, min_samples=1, metric="precomputed", n_jobs=-1)
# dbscan = DBSCAN(eps=0.5, min_samples=1, metric="precomputed", n_jobs=-1)

labels = dbscan.fit_predict(my_graph)

iu.save_result(labels, my_graph, "dice_0.3.txt")
