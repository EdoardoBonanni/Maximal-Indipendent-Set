import numpy as np
import random
import networkx as nx


def greedy_maximal_independent_set(G):
    nx.set_node_attributes(G, False, 'label')
    M = np.empty(shape=0)
    for node in G.nodes:
        if not G.nodes._nodes[node]['label']:
            M = np.append(M, node)
            adjacency = np.array(G.adj[node])
            for adj in adjacency:
                G.nodes._nodes[adj]['label'] = True
    return M


def random_greedy_maximal_independent_set(G):
    nx.set_node_attributes(G, False, 'label')
    M = list()
    random_list = list(G.nodes)
    random.shuffle(random_list)
    for node in random_list:
        if not G.nodes._nodes[node]['label']:
            M.append(node)
            adjacency = list(G.adj[node])
            for adj in adjacency:
                G.nodes._nodes[adj]['label'] = True
    return M


def np_random_greedy_maximal_independent_set(G):
    nx.set_node_attributes(G, False, 'label')
    M = np.empty(shape=0)
    random_np = np.array(G.nodes)
    np.random.shuffle(random_np)
    for node in random_np:
        if not G.nodes._nodes[node]['label']:
            M = np.append(M, node)
            adjacency = np.array(G.adj[node])
            for adj in adjacency:
                G.nodes._nodes[adj]['label'] = True
    return M


def np_random_greedy_maximal_independent_set_boolean_mask(G):
    M = np.empty(shape=0)
    random_np = np.array(G.nodes)
    np.random.shuffle(random_np)
    mask = np.zeros(len(random_np), dtype=bool)
    for i in range(len(random_np)):
        if not mask[i]:
            M = np.append(M, random_np[i])
            adjacency = np.array(G.adj[random_np[i]])
            for adj in adjacency:
                index = np.where(random_np == adj)
                mask[index] = True
    return M


def fast_mis(G):
    mis = np.empty(shape=0)
    nx.set_node_attributes(G, True, 'label')
    nx.set_node_attributes(G, np.empty(shape=0), 'n_values')
    nx.set_node_attributes(G, -1, 'value')

    for node in G.nodes:
        value = random.random()
        G.nodes._nodes[node]['value'] = value
        adjacency = np.array(G.adj[node])
        for adj in adjacency:
            G.nodes._nodes[adj]['n_values'] = np.append(G.nodes._nodes[adj]['n_values'], value)

    for node in G.nodes:
        if G.nodes._nodes[node]['label']:
            n_values = G.nodes._nodes[node]['n_values']
            value = G.nodes._nodes[node]['value']
            if all([value < n_value for n_value in n_values]):
                mis = np.append(mis, node)
                adjacency = np.array(G.adj[node])
                for adj in adjacency:
                    G.nodes._nodes[adj]['label'] = False
    return mis


def mis_nx(G):
    max_independent_set = nx.maximal_independent_set(G, seed=None)
    return max_independent_set


def graphSets(G):
    # Base Case - Given Graph
    # has no nodes
    if len(G.nodes) == 0:
        return []

    # Base Case - Given Graph
    # has 1 node
    if len(G.nodes) == 1:
        return G.nodes

    # Select a vertex from the graph
    random_list = list(G.nodes)
    random.shuffle(random_list)
    node = random_list[0]

    # Case 1 - Proceed removing
    # the selected vertex
    # from the Maximal Set
    H = G.copy()

    # Delete current vertex
    # from the Graph
    H.remove_node(node)

    # Recursive call - Gets
    # Maximal Set,
    # assuming current Vertex
    # not selected

    res1 = graphSets(H)

    # Case 2 - Proceed considering
    # the selected vertex as part
    # of the Maximal Set

    # Loop through its neighbours
    adjacency = np.array(G.adj[node])
    for adj in adjacency:

        # Delete neighbor from
        # the current subgraph
        if adj in H.nodes:
            H.remove_node(adj)

    # This result set contains VFirst,
    # and the result of recursive
    # call assuming neighbors of vFirst
    # are not selected
    res2 = list(graphSets(H))
    res2.append(node)

    # Our final result is the one
    # which is bigger, return it
    if len(res1) > len(res2):
        return res1
    return res2
