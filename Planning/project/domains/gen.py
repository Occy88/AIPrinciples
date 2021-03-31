import numpy as np


def is_in_range(x, y):
    return x < 5 and y < 5 and x>=0 and y>=0

def cts(l):
    return ' x'+str(l[0])+ ' y'+str(l[1])+' '
arrs = [np.array([0, 1]), np.array([0, -1]), np.array([-1, 0]), np.array([1, 0])]
for i in range(0, 5):
    for j in range(0, 5):
        coord = np.array([i, j])
        # print("(cell",'c'+''.join(coord.astype('str').tolist())+')')
        for x in arrs:
            conn = coord + x
            if is_in_range(*conn):
                print("(conn " +cts(coord) + cts(conn) + ')')
