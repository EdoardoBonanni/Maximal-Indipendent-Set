import numpy as np
from itertools import combinations
import json
import networkx as nx
import re
import pickle
import random
import time


def save_graph(obj, name):
    with open(name + ".file", "wb") as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_graph(name):
    with open(name + ".file", "rb") as f:
        obj = pickle.load(f)
        return obj


def add_node(indices, names, G):
    names = np.append(names, indices)
    G.add_node(indices)
    return names


def add_nodes(authors, names, G):
    for author in authors:
        names = np.append(names, author)
        G.add_node(author)
    return names


def find_authors(value):
    if 5 < len(value) < 32 and value.find('-') == -1 and value.find('(') == -1 and value.find(')') == -1 and \
            value.find('[') == -1 and value.find(']') == -1 and value.find(';') == -1 and value.find('\' ') == -1 \
            and not value.startswith(' ') and value[0].isupper() and not any(map(str.isdigit, value)):
        return True
    return False


def create_graph(path, files):
    G = nx.Graph()
    for file in files:
        with open(path + file) as json_file:
            js_file = json.load(json_file)
            if 'formula' in js_file['results'][0]:
                names = np.empty(shape=0)
                formula = js_file['results'][0]['formula']
                for i in range(len(formula)):
                    formula_substring = ''
                    if formula[i].find(' _') != -1:
                        possible_authors = np.empty(shape=0)
                        if re.search(' _(.*)_', formula[i]):
                            formula_substring = formula[i][formula[i].find(' _') + len(' _'):formula[i].rfind('_')]
                            if formula_substring.find('_') != -1:
                                split = formula_substring.split('_')
                                # divide remaining strings
                                possible_authors = np.array([author for author in split if author.find(',') == -1])
                    # search for real authors
                    real_authors = np.array([author for author in possible_authors if find_authors(author)])
                    if real_authors.size:
                        names = add_nodes(real_authors, names, G)
                    elif len(formula_substring) > 0:
                        if find_authors(formula_substring):
                            names = add_node(formula_substring, names, G)
        if len(names) > 1:
            comb = list(combinations(names, 2))
            for i in range(len(comb)):
                if not G.has_edge(comb[i][0], comb[i][1]) and not G.has_edge(comb[i][1], comb[i][0]) and comb[i][0] != comb[i][1]:
                    G.add_edge(comb[i][0], comb[i][1])
    G.remove_nodes_from(list(nx.isolates(G)))
    return G


def shuffle_nodes(G):
    random_nodes = np.array(G.nodes)
    np.random.shuffle(random_nodes)
    return random_nodes


def create_subgraph(G, random_nodes, n_nodes):
    for node in random_nodes[:len(random_nodes) - n_nodes]:
        G.remove_node(node)
