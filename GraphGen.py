import networkx as nx
import random
import copy
import matplotlib.pyplot as plt
import tkinter

class GraphGen:
    """Random Max Degree 4 Graph Generator"""
    def __init__(self, nodes):
        self.n = nodes
    def g(self):
        while True:
            try:
                seq = seqGen(self.n)
                g = nx.random_degree_sequence_graph(seq)
                break
            except nx.NetworkXError:
                pass
        for e in g.edges():
            g[e[0]][e[1]]['w'] = random.randint(1, 2**self.n)

        return g
    def gPoljak(self):
        g = nx.random_regular_graph(4, self.n)
        for e in g.edges():
            g[e[0]][e[1]]['w'] = random.randint(1, 2**self.n)
        return g

def seqGen(n):
    seq = [1,2] #start with invalid deg seq
    while not nx.is_valid_degree_sequence(seq):
        seq = []
        for x in range(0,n):
            seq.append(random.randint(1,4))
    return seq
