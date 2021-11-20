import numpy as np
import networkx as nx
import operator
from networkx.algorithms.core import core_number


def all_mis_nx(G):
    all_mis = list(nx.find_cliques(G))
    return all_mis


def BK1(complement_graph, P, R, X, all_mis):
    if len(np.union1d(P, X)) == 0:
        all_mis.append(R)
        return
    for v in P:
        adjacency = np.array(complement_graph.adj[v])
        BK1(complement_graph, np.intersect1d(P, adjacency), np.union1d(R, v), np.intersect1d(X, adjacency), all_mis)
        P = np.setdiff1d(P, v)
        X = np.append(X, v)


def BK1_set(complement_graph, P, R, X, all_mis):
    if not P and not X:
        all_mis.append(R)
        return
    while P:
        v = P.pop()
        adjacency = set(complement_graph.adj[v])
        BK1_set(complement_graph, P.intersection(adjacency), R.union({v}), X.intersection(adjacency), all_mis)
        X.add(v)


def BK2(complement_graph, P, R, X, all_mis):
    if len(np.union1d(P, X)) == 0:
        all_mis.append(R)
        return
    union = np.union1d(P, X)
    # pivot u
    u = union[np.argmax([len(np.intersect1d(P, complement_graph.adj[u])) for u in union])]
    for v in np.setdiff1d(P, complement_graph.adj[u]):
        adjacency = np.array(complement_graph.adj[v])
        BK2(complement_graph, np.intersect1d(P, adjacency), np.union1d(R, v), np.intersect1d(X, adjacency), all_mis)
        P = np.setdiff1d(P, v)
        X = np.append(X, v)


def BK2_set(complement_graph, P, R, X, all_mis):
    if not P and not X:
        all_mis.append(R)
        return
    union = list(P.union(X))
    # pivot u
    u = union[np.argmax([len(P.intersection(set(complement_graph.adj[u]))) for u in union])]
    while P.difference(set(complement_graph.adj[u])):
        v = P.pop()
        adjacency = set(complement_graph.adj[v])
        BK2_set(complement_graph, P.intersection(adjacency), R.union({v}), X.intersection(adjacency), all_mis)
        X.add(v)


def BKD(complement_graph, P, X, all_mis):
    # degeneracy ordering
    deg_order = list(core_number(complement_graph).items())
    for i, v in enumerate(deg_order):
        adjacency = np.array(complement_graph.adj[v[0]])
        P = np.intersect1d(adjacency, list(map(operator.itemgetter(0), deg_order[i + 1:])))
        X = np.intersect1d(adjacency, list(map(operator.itemgetter(0), deg_order[0:i])))
        BK2(complement_graph, P, v[0], X, all_mis)


def BKD_set(complement_graph, P, X, all_mis):
    # degeneracy ordering
    deg_order = list(core_number(complement_graph).items())
    for i, v in enumerate(deg_order):
        adjacency = set(complement_graph.adj[v[0]])
        P = adjacency.intersection(set(map(operator.itemgetter(0), deg_order[i + 1:])))
        X = adjacency.intersection(set(map(operator.itemgetter(0), deg_order[0:i])))
        BK2_set(complement_graph, P, {v[0]}, X, all_mis)
