#testing feasibility of Poljak's (SICOMP 1995) method on finite simple graphs with
#maximum degree 4. outputs objective function vector c and matrix m as text file
#for input into mathematica LinearProgramming(c,m,b,lu,dom) solver.
#
#IP formulation: given graph G with n vertices V(G) = {0, 1, ..., n-1}
#                minimize: x_{n}
#                subject to: inequality determined in classifyNode for all v in V(G)
#                            x_{n} >= x_{i} for all i from 0 to n - 1
#
#hence encoding that we want to minimize the maximum edge weight

#components:
#inequality determination
#constraint matrix construction
#contraint matrix check
#mathematica code output
#note: g.edges() always lists edges in increasing lexicographic order

import networkx as nx
import random
import copy
import numpy as np
import subprocess
import re
#custom packages:
import GraphGen
import bruteForceLocalMaxCut
import Verifier

def main():
    nodes = 5
    gen = GraphGen.GraphGen(nodes)
    g = gen.random4RegularGraph()

    (m, b, mArr, bArr, x) = create_mbx(g)
    c = createC(g)
    checkIP(mArr, bArr, x)

    f = open('ip.m', 'w') #write mathematica script
    f.write("Print[LinearProgramming[" + c + ", " + m
            + ", " + b + ", " + "0" + ", " + "Integers]]")
    f.close()

    solution = executeMathematicaScript()

    gNewWeights = makeNewG(g, solution)

    print(checkNewG(gNewWeights, g))

def checkNewG(newG, g):
    localMaxima = bruteForceLocalMaxCut(g).findLocalMinima()
    verifier = Verifier(newG)
    for partition in localMaxima:
        result, nodeSet = verifier.partitionCheck(partition)
        if result == False:
            return False
    return True

def makeNewG(g, solution):
    gNew = g.copy()
    pointer = 0
    for (u, v) in gNew.edges():
        gNew[u][v]['w'] = solution[pointer]
        pointer += 1
    return gNew

def executeMathematicaScript():
    mathOutput = str(subprocess.check_output(['math', '-script', 'ip.m']))
    solution = convertStringtoList(mathOutput)
    return(solution)

def convertStringtoList(mathOutput):
    pattern = "(?:\{|,\s)(\d+)"
    solution = []
    outputStr = re.findall(pattern, mathOutput)
    print(outputStr)
    for entry in outputStr:
        solution.append(int(entry))
    return solution

def checkIP(m, b, x): #check that the IP mx>=b is valid
    m = np.matrix(m)
    x = np.matrix(x) #vector with original edge weights
    b = np.matrix(b)
    compare = np.greater_equal(m * np.transpose(x), np.transpose(b))
    assert not np.in1d(False, compare)[0] #see if mx>=b not true

def create_mbx(g):
    e = list(g.edges())
    m = "{"
    mArr = [] #array version for verification purposes
    b = []
    x = []
    for (u, v) in e: #create verification vector with original edge weights
        x.append(g[u][v]['w'])
    x.append(max(x)) #max edge weight as max variable
    for v in g:
        eList = [] #list of incident edges
        for nbr in g[v]: #creating ordered tuples (needed to index properly)
            if nbr < v:
                eList.append((nbr, v))
            else:
                eList.append((v, nbr))
        eList.sort(key=lambda x: g[x[0]][x[1]]['w']) #ascending order
        wList = [] #list of edge weights
        for (u, v) in eList:
            wList.append(g[u][v]['w'])

        nodeType = classifyNode(wList)
        line1 = [0] * (len(g.edges) + 1) #create list of 0s to represent row in matrix
        line2 = [0] * (len(g.edges) + 1)
        two = True #need two rows in matrix?
        if nodeType == 1:
            line1[e.index(eList[0])] = 1
            line1[e.index(eList[1])] = 1
            line1[e.index(eList[2])] = -1
            line1[e.index(eList[3])] = 1
            b.append(1)
            line2[e.index(eList[0])] = 1
            line2[e.index(eList[1])] = 1
            line2[e.index(eList[2])] = 1
            line2[e.index(eList[3])] = -1
            b.append(1)

        elif nodeType == 2:
            line1[e.index(eList[0])] = -1
            line1[e.index(eList[1])] = -1
            line1[e.index(eList[2])] = -1
            line1[e.index(eList[3])] = 1
            b.append(1)
            two = False
        elif nodeType == 3:
            line1[e.index(eList[0])] = -1
            line1[e.index(eList[1])] = 1
            line1[e.index(eList[2])] = 1
            line1[e.index(eList[3])] = -1
            b.append(1)
            two = False
        elif nodeType == 4:
            line1[e.index(eList[0])] = 1
            line1[e.index(eList[1])] = 1
            line1[e.index(eList[2])] = 1
            line1[e.index(eList[3])] = -1
            b.append(0)
            line2[e.index(eList[0])] = -1
            line2[e.index(eList[1])] = -1
            line2[e.index(eList[2])] = -1
            line2[e.index(eList[3])] = 1
            b.append(0)
        elif nodeType == 5:
            line1[e.index(eList[0])] = 1
            line1[e.index(eList[1])] = -1
            line1[e.index(eList[2])] = -1
            line1[e.index(eList[3])] = 1
            b.append(0)
            line2[e.index(eList[0])] = -1
            line2[e.index(eList[1])] = 1
            line2[e.index(eList[2])] = 1
            line2[e.index(eList[3])] = -1
            b.append(0)
        if two:
            m += "{" + str(line1)[1:-1] + "}, "
            m += "{" + str(line2)[1:-1] + "}, "
            mArr.append(line1)
            mArr.append(line2)
        else:
            m += "{" + str(line1)[1:-1] + "}, "
            mArr.append(line1)

    bArr = copy.deepcopy(b) #array version for verification purposes
    b = str(b)
    b = "{" + b[1:-1] + ", 0" * len(g.edges) + "}" #add extra var constraits
    bArr = bArr + [0] * len(g.edges)

    for q in range(0, len(g.edges)):
        m += "{" + "0, " * q + "-1, " + "0, " * (len(g.edges) - q - 1) + "1}, "
        mArr.append([0] * q + [-1] + [0] * (len(g.edges) - q - 1) + [1])
    m = m[0:-2]
    m += "}"
    return (m, b, mArr, bArr, x)

def classifyNode(wList):
    a = wList[3]
    b = wList[2]
    c = wList[1]
    d = wList[0]

    if ((a+d>b+c) and (a < b + c +d)):
        return 1
    elif a > b + c + d:
        return 2
    elif (a + d < b + c):
        return 3
    elif a == b + c + d:
        return 4
    elif a + d == b + c:
        return 5
    else:
        print('failed to classify')

def createC(g):
    c = "{" + "0, " * len(g.edges) + "1}"
    return c

if __name__ == '__main__':
    main()
