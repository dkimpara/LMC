#solution verifier, error identification, and graphdisplay for algTest

import networkx as nx
import random
import copy
import matplotlib.pyplot as plt
import tkinter

class Verifier:
    """Verifies solution/checks answers and displays failed cases"""
    def partitionCheck(self, g, partition):
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

    def graphDisplay(self, g, partition, nodeSet): #display graph with the partition

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
