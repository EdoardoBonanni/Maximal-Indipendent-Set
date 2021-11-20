import enumerate_MIS
import numpy as np
import time


def prepare_nx(G):
    # G is the complement_graph
    start = time.time()
    all_mis_nx = enumerate_MIS.all_mis_nx(G)
    print('Execution time nx =', time.time() - start, 'secs')
    return all_mis_nx


def prepare_BK1(G):
    # G is the complement_graph
    all_mis_BK1 = []
    P = np.array(G.nodes)
    R = np.empty(shape=0)
    X = np.empty(shape=0)
    start = time.time()
    enumerate_MIS.BK1(G, P, R, X, all_mis_BK1)
    print('Execution time BK1 =', time.time() - start, 'secs')
    return all_mis_BK1


def prepare_BK2(G):
    # G is the complement_graph
    all_mis_BK2 = []
    P = np.array(G.nodes)
    R = np.empty(shape=0)
    X = np.empty(shape=0)
    start = time.time()
    enumerate_MIS.BK2(G, P, R, X, all_mis_BK2)
    print('Execution time BK2 =', time.time() - start, 'secs')
    return all_mis_BK2


def prepare_BK1_set(G):
    # G is the complement_graph
    all_mis_BK1_set = []
    P = set(G.nodes)
    R = set()
    X = set()
    start = time.time()
    enumerate_MIS.BK1_set(G, P, R, X, all_mis_BK1_set)
    print('Execution time BK1_set =', time.time() - start, 'secs')
    return all_mis_BK1_set


def prepare_BK2_set(G):
    # G is the complement_graph
    all_mis_BK2_set = []
    P = set(G.nodes)
    R = set()
    X = set()
    start = time.time()
    enumerate_MIS.BK2_set(G, P, R, X, all_mis_BK2_set)
    print('Execution time BK2_set =', time.time() - start, 'secs')
    return all_mis_BK2_set


def prepare_BKD(G):
    # G is the complement_graph
    P = np.empty(shape=0)
    X = np.empty(shape=0)
    all_mis_BKD = []
    start = time.time()
    enumerate_MIS.BKD(G, P, X, all_mis_BKD)
    print('Execution time BKD =', time.time() - start, 'secs')
    return all_mis_BKD


def prepare_BKD_set(G):
    # G is the complement_graph
    P = set()
    X = set()
    all_mis_BKD_set = []
    start = time.time()
    enumerate_MIS.BKD_set(G, P, X, all_mis_BKD_set)
    print('Execution time BKD_set =', time.time() - start, 'secs')
    return all_mis_BKD_set
