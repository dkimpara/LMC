import networkx as nx
import random
import copy
import matplotlib.pyplot as plt
import tkinter

import GraphGen
import Verifier

#testing feasibility of Poljak's (SICOMP 1995) method applied to graphs with maximum
#degree 4. outputs objective function vector c and matrix m as text file
#for input into mathematica LinearProgramming(c,m,b,lu,integer) solver.

#components:
#inequality determination
#constraint matrix construction


def main(nodes):
    gen = GraphGen.GraphGen(nodes)
    g = gen.gPoljak()
    print(g)
    f = open('ip.txt', 'w')
    mAndb = createMandB(g)

    f.write("LinearProgramming[" + createC(g) + ", " + mAndb[0]
            + ", " + mAndb[1] + ", " + "0" + ", " + "Integers]")
    f.close()

def createB(g):
    return "{" + len(g.edges)*" 0," + "0}"

def createMandB(g):
    e = list(g.edges())
    m = "{"
    b = []
    for v in g:
        eList = [] #list of incident edges
        for nbr in g[v]: #creating ordered tuples (needed to index properly)
            if nbr < v:
                eList.append((nbr, v))
            else:
                eList.append((v, nbr))
        eList.sort(key=lambda x: g[x[0]][x[1]]['w']) #ascending order
        wList = [] #list of edge weights
        for edge in eList:
            wList.append(g[edge[0]][edge[1]]['w'])

        nodeType = classifyNode(wList)
        line1 = [0] * (len(g.edges) + 1) #create list of 0s to represent row in matrix
        line2 = [0] * (len(g.edges) + 1)
        two = True #need two lines in matrix?
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
        else:
            m += "{" + str(line1)[1:-1] + "}, "

    b = str(b)
    b = "{" + b[1:-1] + ", 0}"
    m += "{" + len(g.edges)*"-1, " + "1}}"
    return (m, b)

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
    c = "{" + "0, "*len(g.edges) + "1}"
    return c

if __name__ == '__main__':
    main(5)
