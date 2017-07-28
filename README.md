# localMaxCut
Local Max-Cut algorithm test environment with Python package NetworkX

Author: Dhamma Kimpara

Python 3.5.2

Packages: NetworkX, random, copy, matplotlib, tkinter, numpy

AMS subject classifications: 68Q25, 90C10, 90C27

Problem setting:
---------
The complexity of local max-cut with FLIP-neighborhood 
is known for finite simple graphs with maximum degree 3 and maximum degree 
5 and above. Hence we attempt to establish a polynomial time algorithm for 
graphs with maximum degree 4. (Elsaesser, Tobias)


Objective 1:
--------
files: poljakTest.py, GraphGen.py, deg4char.py

Testing feasibility of Poljak's (SICOMP 1995) method on finite simple graphs with
maximum degree 4. outputs objective function vector c and matrix m as text file
for input into mathematica LinearProgramming(c,m,b,lu,dom) solver.


Objective 2:
-----------
files: algTest.py, Alg.py, Verifier.py

Provided test environment for problem with algorithm input, solution verifier,
error identification, and graph display. 


References:
----------
Poljak, S. 1995: http://dl.acm.org/citation.cfm?id=210959

Elsaesser, Tobias: https://arxiv.org/abs/1004.5329 for an overview


------
Work done at Operations Research at the Technical University of Munich
