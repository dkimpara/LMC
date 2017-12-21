import networkx as nx
import random
import copy
import matplotlib.pyplot as plt
import tkinter

class Alg:
    '''user defined algorithm to be tested'''
    def localCutAlg(self, g): #g graph with edge weights
        for v in g:
            g.node[v]['c'] = 0
            for nbr in g[v]:
                g.node[v]['c'] += g[v][nbr]['w']
        nodes = list(g.nodes())
        nodes.sort(key=lambda x: g.node[x]['c'], reverse= True)

        partition = [nodes.pop(0)]
        complement = nodes
        for u in complement:
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
