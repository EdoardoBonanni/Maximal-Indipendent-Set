from os import listdir
from os.path import isfile, join
import utils, find_MIS, enumerate_MIS, prepare_algorithms as pa
import time
import networkx as nx
import timeit
import numpy as np


def main():
    create_graph = False
    run_find_MIS = False
    run_enumerate_MIS = True
    if create_graph:
        path = 'sequences/'
        files = [f for f in listdir(path) if isfile(join(path, f))]

        # Total nodes = 1096, 1012 nodes for connected graph
        G = utils.create_graph(path, files)
        # utils.save_graph(G, "authors_graph")
        utils.save_graph(G, "graphs/authors_connected_graph")
    else:
        G = utils.load_graph("graphs/authors_connected_graph")

    if run_find_MIS:

        iterations = 30
        print('Run_find_MIS: ')
        print('Average execution time nx_mis =', (
            timeit.timeit("find_MIS.mis_nx(G)", "import find_MIS", globals={'G': G}, number=iterations)) / iterations,
              'secs')
        print('Average execution time random_greedy_mis =', (
            timeit.timeit("find_MIS.random_greedy_maximal_independent_set(G)", "import find_MIS", globals={'G': G},
                          number=iterations)) / iterations, 'secs')
        print('Average execution time np_random_greedy_mis =', (
            timeit.timeit("find_MIS.np_random_greedy_maximal_independent_set(G)", "import find_MIS", globals={'G': G},
                          number=iterations)) / iterations, 'secs')
        print('Average execution time np_random_greedy_boolean_mask_mis =', (
            timeit.timeit("find_MIS.np_random_greedy_maximal_independent_set_boolean_mask(G)", "import find_MIS",
                          globals={'G': G}, number=iterations)) / iterations, 'secs')
        print('Average execution time fast_mis =', (
            timeit.timeit("find_MIS.fast_mis(G)", "import find_MIS", globals={'G': G}, number=iterations)) / iterations,
              'secs')

        # P = np.array(G.nodes)
        # R = np.empty(shape=0)
        # X = np.empty(shape=0)

        # print('Average execution time BK1_mis =', ( timeit.timeit("find_MIS.BK1_mis(G, P, R, X)",
        # "import find_MIS", globals={'G': G, 'P': P, 'R': R, 'X': X}, number=iterations)) / iterations, 'secs')

        # print('Average execution time BK2_mis =', ( timeit.timeit("find_MIS.BK2_mis(G, P, R, X)",
        # "import find_MIS", globals={'G': G, 'P': P, 'R': R, 'X': X}, number=iterations)) / iterations, 'secs')

        # print('Average execution time BKD_mis =', ( timeit.timeit("find_MIS.BKD_mis(G, P, X)",
        # "import find_MIS", globals={'G': G, 'P': P, 'X': X}, number=iterations)) / iterations, 'secs')

    if run_enumerate_MIS:
        # random_nodes = utils.shuffle_nodes(G)
        # n_nodes_subgraph = 20
        # utils.create_subgraph(G, random_nodes, n_nodes_subgraph)
        # complement_graph = nx.complement(G)

        complement_graph = utils.load_graph("graphs/compl_subgraph100")

        if run_find_MIS:
            print('')
        print('Run_enumerate_MIS: ')

        all_mis_nx = pa.prepare_nx(complement_graph)
        # all_mis_BK1 = pa.prepare_BK1(complement_graph)
        # all_mis_BK1_nocomplement = pa.prepare_BK1_nocomplement(G)
        all_mis_BK2 = pa.prepare_BK2(complement_graph)
        # all_mis_BK2_nocomplement = pa.prepare_BK2_nocomplement(G)
        #
        # all_mis_BK1_set = pa.prepare_BK1_set(complement_graph)
        # all_mis_BK2_set = pa.prepare_BK2_set(complement_graph)

        # all_mis_BKD = pa.prepare_BKD(complement_graph)
        # all_mis_BKD_set = pa.prepare_BKD_set(complement_graph)

        max_mis = max(all_mis_nx, key=len)

    print('Fine')


if __name__ == '__main__':
    main()
