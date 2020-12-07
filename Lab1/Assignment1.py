import random
import numpy as np
import sys
from FinalProject.NQueens_implementation import NQueensProblem
print(sys.version)
p = NQueensProblem(8)
print(p)
n = 8


# p.initial = tuple(random.randint(0, n - 1) for i in range(n))
# print(p.initial)
# print(p.value(p.initial))
# print(diPasswordr(p))
#

def hill_climbing(p: NQueensProblem):
    def get_max_values(actions, state):
        v = np.zeros((p.N,), dtype=int)
        # print('array init:', v)
        for index, a in enumerate(actions):
            # print(state, a)
            v[index] = p.value(p.result(state, a))
        # print("=======MAX VALUES============")
        m = np.min(v)
        # print(v)
        # print(m)
        # print("================")
        # print(np.where(v == m)[0])
        return np.where(v == m)[0], m

    c = p.initial
    v_max = p.value(c)
    # print(v_max)
    c_max = c
    for i in range(p.N):
        actions = p.actions(p.initial)
        # print(actions)
        indices, val = get_max_values(actions, c_max)
        # print('checking max', val, v_max)
        if val < v_max:
            v_max = val
            # print('max detected')
            # print(actions)
            c_max = p.result(c_max, actions[random.choice(indices)])
        else:
            return v_max, c_max
    return v_max, c_max


a = set()
s = 0
for n in range(10000):
    r = hill_climbing(p)
    if r[0] == 0:
        a.add(r[1])
        s += 1
print(s)
print(len(a))
exit(0)


