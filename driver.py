import networkx as nx
import random
import copy
import matplotlib.pyplot as plt
import tkinter

def createG(n): #generate random 4 regular graph with n vertices

    #g = nx.random_regular_graph(4, n, seed= None)
    while True:
        try:
            seq = seqGen(n)
            g = nx.random_degree_sequence_graph(seq)
            break
        except nx.NetworkXError:
            pass
    for e in g.edges():
        g[e[0]][e[1]]['w'] = random.randint(0, 2**n)

    return g

def seqGen(n):
    seq = [1,2]
    while not nx.is_valid_degree_sequence(seq):
        seq = []
        for x in range(0,n):
            seq.append(random.randint(1,4))
    return seq

def localCutAlg(g):
    for v in g:
        g.node[v]['c'] = 0
        for nbr in g[v]:
            g.node[v]['c'] += g[v][nbr]['w']
    nodes = list(g.nodes())
    nodes.sort(key=lambda x: g.node[x]['c'], reverse= True)
    partition = [nodes.pop(0)] #nodes is now the complement of partition
    for u in nodes:
        connected = False
        adj = 0
        for v in partition:
            if (u,v) in g.edges():
                connected = True
                adj += g[u][v]['w']

        if not connected:
            partition.append(u)
        elif g.node[u]['c'] > 2*adj:
            partition.append(u)

    return partition

def partitionCheck(g, partition):
#checks partition for local search optimality
#returns nodeset that increases cut
    algResult = nx.cut_size(g, set(partition), T=None, weight = 'w')
    result = True
    nodeSet = []
    for v in g:
        p = copy.deepcopy(partition)
        if v in partition:
            p.remove(v)
        else:
            p.append(v)
        p = set(p)
        neighborCut = nx.cut_size(g, p, T=None, weight='w')

        if neighborCut > algResult:
            result = False
            nodeSet.append((v, neighborCut))
    return (result, nodeSet)

def graphDisplay(g, partition, nodeSet): #display graph with the partition

    complement = []
    for v in g:
        if v not in partition:
            complement.append(v)

    plt.close()
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, nodelist = partition, node_color='r')
    nx.draw_networkx_nodes(g, pos, nodelist = complement, node_color='b')
    nx.draw_networkx_labels(g, pos)

    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_edge_labels(g, pos, edge_labels = g.edges())

    print(nodeSet)
    plt.show()


n = 5

for k in range(0,10):
    g = createG(n)
    partition = localCutAlg(g)
    result = partitionCheck(g, partition)
    if len(result[1])>1:
        graphDisplay(g, partition, result[1])
