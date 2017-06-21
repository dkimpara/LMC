import networkx as nx
import random
import copy
import matplotlib.pyplot as plt
import tkinter

n = 12

def createG(n): #generate random 4 regular graph with n vertices
    g = nx.random_regular_graph(4, n, seed= None)

    for e in g.edges():
        g[e[0]][e[1]]['weight'] = random.randint(0, 2**n)

    return g

def localCutAlg(g):
    for v in g:
        g.node[v]['c'] = 0
        for nbr in g[v]:
            g.node[v]['c'] += g[v][nbr]['weight']
    nodes = list(g.nodes())
    nodes.sort(key=lambda x: g.node[x]['c'], reverse= True)

    partition = [nodes.pop(0)]

    #for u in nodes:

        #if
    return partition

def partitionCheck(g, partition):
#checks partition for local search optimality
#returns nodeset that increases cut
    algResult = nx.cut_size(g, partition, weight = 'weight')
    result = True
    nodeSet = []
    for v in g:
        print(v)
        p = copy.deepcopy(partition)
        if v in partition:
            p.remove(v)
        else:
            p.append(v)
            print(p)
        neighborCut = nx.cut_size(g, p, 'weight')
        if neighborCut > algResult:
            result = False
            nodeSet.append(v)
    return (result, nodeSet)

def graphDisplay(g, partition, nodeSet): #display graph with the partition
    print(nodeSet)

for k in range(0,1):
    g = createG(n)
    partition = localCutAlg(g)
    result = partitionCheck(g, partition)
    if not result[0]:
        graphDisplay(g, partition, result[1])
