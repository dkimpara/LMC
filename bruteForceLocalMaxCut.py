#semi-brute force algorithm for all local maxima
import networkx as nx
from itertools import chain, combinations
from math import ceil

import random
import copy
import numpy as np
import subprocess
import re
#custom packages
import Verifier

class bruteForceLocalMaxCut:
    """find all local maxima in graph g"""
    def __init__(self, g):
        self.g = g

    def findLocalMinima(self):
        n = self.g.order()
        verifier = Verifier(self.g)
        localMaxList = []

        pset = powerset(n)
        print(powerset)

        for subset in pset:
            result, nodeSet = verifier.partitionCheck(list(subset))
            if result == True:
                localMaxList.append(subset)
        return(localMaxList) #return list of subsets that are local max


def powerset(n):
    ptuple = chain.from_interable(combinations(list(range(n)),
            x) for x in range(ceil((n + 1)/2)) #need only to check up to halfsize subsets
    return map(set, ptuple) #returns list of subsets
