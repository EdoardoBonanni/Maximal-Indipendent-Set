import time

import numpy as np
import networkx as nx
import operator
import heapq as hq


def all_mis_nx(G):
    all_mis = list(nx.find_cliques(G))
    return all_mis


def BK1(G, P, R, X, all_mis):
    if len(np.union1d(P, X)) == 0:
        all_mis.append(R)  # maximal clique
        return
    for v in P:
        adjacency = np.array(G.adj[v])
        BK1(G, np.intersect1d(P, adjacency), np.union1d(R, v), np.intersect1d(X, adjacency), all_mis)
        P = np.setdiff1d(P, v)
        X = np.append(X, v)


def BK2(G, P, R, X, all_mis):
    if len(np.union1d(P, X)) == 0:
        all_mis.append(R)  # maximal clique
        return
    union = np.union1d(P, X)
    u = union[np.argmax([len(np.intersect1d(P, G.adj[u])) for u in union])]
    for v in np.setdiff1d(P, G.adj[u]):
        adjacency = np.array(G.adj[v])
        BK2(G, np.intersect1d(P, adjacency), np.union1d(R, v), np.intersect1d(X, adjacency), all_mis)
        P = np.setdiff1d(P, v)
        X = np.append(X, v)


def BK1_set(G, P, R, X, all_mis):
    if not P and not X:
        all_mis.append(R)
        return
    while P:
        v = P.pop()
        adjacency = set(G.adj[v])
        BK1_set(G, P.intersection(adjacency), R.union({v}), X.intersection(adjacency), all_mis)
        X.add(v)


def BK2_set(G, P, R, X, all_mis):
    if not P and not X:
        all_mis.append(R)
        return
    union = list(P.union(X))
    u = union[np.argmax([len(P.intersection(set(G.adj[u]))) for u in union])]
    while P.difference(set(G.adj[u])):
        v = P.pop()
        adjacency = set(G.adj[v])
        BK2_set(G, P.intersection(adjacency), R.union({v}), X.intersection(adjacency), all_mis)
        X.add(v)


def BKD(G, all_mis):
    P = np.empty(shape=0)
    X = np.empty(shape=0)
    # degeneracy ordering
    deg_order = sorted(G.degree, key=lambda x: x[1])
    for i, v in enumerate(deg_order):
        adjacency = np.array(G.adj[v[0]])
        P = np.intersect1d(adjacency, list(map(operator.itemgetter(0), deg_order[i + 1:])))
        X = np.intersect1d(adjacency, list(map(operator.itemgetter(0), deg_order[0:i])))
        BK2(G, P, v[0], X, all_mis)


def BKD_set(G, all_mis):
    P = set()
    X = set()
    # degeneracy ordering
    deg_order = sorted(G.degree, key=lambda x: x[1])
    for i, v in enumerate(deg_order):
        adjacency = set(G.adj[v[0]])
        P = adjacency.intersection(set(map(operator.itemgetter(0), deg_order[i + 1:])))
        X = adjacency.intersection(set(map(operator.itemgetter(0), deg_order[0:i])))
        BK2_set(G, P, {v[0]}, X, all_mis)
