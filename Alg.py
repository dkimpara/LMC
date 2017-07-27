import networkx as nx
import random
import copy
import matplotlib.pyplot as plt
import tkinter

class Alg:
    def localCutAlg(self, g):
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
