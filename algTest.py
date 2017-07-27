import networkx as nx
import random
import copy
import matplotlib.pyplot as plt
import tkinter

import GraphGen
import Alg
import Verifier


def main(nodes, numberOfTests):
    for k in range(0,numberOfTests):
        gen = GraphGen(nodes)
        g = gen.g()
        partition = Alg.localCutAlg(g)
        result = Verifier.partitionCheck(g, partition)
        if len(result[1])>1:
            Verifier.graphDisplay(g, partition, result[1])
