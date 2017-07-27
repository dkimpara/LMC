import random
import math
for i in range(0, 10000):
    s = []
    for x in range(0,4):
        s.append(math.ceil(random.expovariate(0.005)))
    s.sort()
    a = s[3]
    b = s[2]
    c = s[1]
    d = s[0]

    if a > b + c + d:
        pass
    elif ((a+d>b+c) and (a < b + c +d)):
        pass
    elif (a + d < b + c):
        pass
    elif a == b + c + d:
        pass
    elif a + d == b + c:
        pass
    else:
        print(s)
