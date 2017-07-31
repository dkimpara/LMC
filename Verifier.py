#solution verifier, error identification, and graphdisplay for algTest

import networkx as nx
import random
import copy
import matplotlib.pyplot as plt
import tkinter

class Verifier:
    """Verifies solution/checks answers and displays failed cases"""
    def __init__(self, g):
        self.g = g

    def partitionCheck(self, partition):
    #checks partition for local search optimality
    #returns nodeset that increases cut
        algResult = nx.cut_size(self.g, set(partition), T=None, weight = 'w')
        result = True
        nodeSet = []
        for v in self.g:
            p = copy.deepcopy(partition)
            if v in partition:
                p.remove(v)
            else:
                p.append(v)
            p = set(p)
            neighborCut = nx.cut_size(self.g, p, T=None, weight='w')

            if neighborCut > algResult:
                result = False
                nodeSet.append((v, neighborCut))
        return (result, nodeSet)

    def graphDisplay(self, partition, nodeSet): #display graph with the partition
        complement = []
        for v in self.g:
            if v not in partition:
                complement.append(v)

        plt.close()
        pos = nx.spring_layout(self.g)
        nx.draw_networkx_nodes(self.g, pos, nodelist = partition, node_color='r')
        nx.draw_networkx_nodes(self.g, pos, nodelist = complement, node_color='b')
        nx.draw_networkx_labels(self.g, pos)

        nx.draw_networkx_edges(self.g, pos)
        nx.draw_networkx_edge_labels(self.g, pos, edge_labels = self.g.edges())

        print(nodeSet)
        plt.show()
