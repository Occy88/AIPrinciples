import math
import os
import queue
import time
from copy import deepcopy

AGENT_SYMBOL = 'A'
GOAL_SYMBOL = 'G'
WALL_SYMBOL = '#'
VISITED_CELL_SYMBOL = 'V'
EXPANDED_NOT_VISITED_CELL_SYMBOL = 'E'
EMPTY_SYMBOL = ' '

print_rate_per_sec = 1
agent_coord = [1, 3]
goal_coord = [4, 7]
initial_map = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', ' ', ' ', 'A', ' ', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', '#', '#', '#'],
    ['#', ' ', '#', '#', '#', ' ', '#', ' ', '#'],
    ['#', ' ', '#', ' ', '#', ' ', ' ', 'G', '#'],
    ['#', ' ', ' ', ' ', '#', ' ', '#', '#', '#'],
    ['#', ' ', '#', ' ', '#', ' ', ' ', ' ', '#'],
    ['#', ' ', '#', ' ', '#', '#', '#', ' ', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#']]
L, LU, U, RU, R, RD, D, LD = [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1]
adj = (L, U, R, D)
diag = (LU, RU, RD, LD)
adj_diag = adj + diag


def print_map():
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in current_map:
        print(str(row))
        # s1 = ''
        # for item in row:
        #
        #     if item == WALL_SYMBOL:
        #         format = ';'.join([str(1), str(30)])
        #         s1 += u'\x1b[%sm \u25A8\x1b[0m' % (format)
        #     elif item == EXPANDED_NOT_VISITED_CELL_SYMBOL:
        #         format = ';'.join([str(1), str(33)])
        #         s1 += u'\x1b[%sm \u25CF\x1b[0m' % (format)
        #     elif item == VISITED_CELL_SYMBOL:
        #         format = ';'.join([str(1), str(31)])
        #         s1 += u'\x1b[%sm \u25CF\x1b[0m' % (format)
        #     else:
        #         format = ';'.join([str(1), str(30)])
        #         s1 += u'\x1b[%sm %s\x1b[0m' % (format, item)
        # print(s1)
    time.sleep(print_rate_per_sec)


def valid_cell(row, col):
    return row >= 0 and row < len(current_map) and col >= 0 and col < len(current_map[0]) and current_map[row][
        col] is not WALL_SYMBOL and current_map[row][col] is not VISITED_CELL_SYMBOL


# ASSUMING POS+[COL,ROW]: column is right left, row is up down


# can't use numpy so a couple extra function to make life easier:
def s(p1, p2):
    return [p1[0] + p2[0], p1[1] + p2[1]]


def generate_adjacent_cells(point, cells=adj):
    return list(s(cell, point) for cell in cells if valid_cell(*s(cell, point)))


def l2norm(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def order_by_heuristic(points, goal, func=l2norm):
    """
    returns the points sorted by the heuristic function and goal
    the order of points that best match the function.
    """
    scores = [func(*point, *goal) for point in points]
    sorted_indices = sorted(range(len(scores)), key=lambda k: scores[k])
    return list(map(lambda k: points[k], sorted_indices))


def BFS(point, adjacent_cells=adj):
    q = queue.Queue()
    q.put(point)
    while not q.empty():
        potential = q.get()
        if goal_coord == potential:
            current_map[potential[0]][potential[1]] = AGENT_SYMBOL
            print_map()
            return True
        current_map[potential[0]][potential[1]] = VISITED_CELL_SYMBOL
        expand = generate_adjacent_cells(potential, cells=adjacent_cells)
        list = [q.put(cell) for cell in expand]
        for cell in expand:
            current_map[cell[0]][cell[1]] = EXPANDED_NOT_VISITED_CELL_SYMBOL
        print_map()

    return False


def DFS(agent_coord, heuristic=None, adjacent_cells=adj):
    """
    heuristic: function by which to sort points (order of exploration)
    y,x: point where to start
    cells: which cells to expand list of vectors to som onto point (y,x)+cell -> (y',x')
    """
    # set agent coord to agent coord
    current_map[agent_coord[0]][agent_coord[1]] = AGENT_SYMBOL
    # set agent coord cell to visited

    # Check if the current state is goal state
    if agent_coord == goal_coord:
        print_map()
        return True
    # get adjacent valid cells
    cells = generate_adjacent_cells(agent_coord, cells=adjacent_cells)
    if len(cells) <= 0:
        current_map[agent_coord[0]][agent_coord[1]] = VISITED_CELL_SYMBOL
        print_map()
        print("GOAL FOUND")
        return False

    # check if heuristic is mentioned
    if heuristic is not None:
        cells = order_by_heuristic(cells, goal_coord, heuristic)
    #   set cells to expanded
    print(cells)

    for cell in cells:
        current_map[cell[0]][cell[1]] = EXPANDED_NOT_VISITED_CELL_SYMBOL
    print_map()
    current_map[agent_coord[0]][agent_coord[1]] = VISITED_CELL_SYMBOL

    # call dfs on all cells to isit.
    for cell in cells:
        if DFS(cell, heuristic=heuristic, adjacent_cells=adjacent_cells):
            return True
    print("GOAL NOT FOUND")
    return False


while True:
    current_map = deepcopy(initial_map)
    print_map()
    cmd = input("Commands:\ndfs\ndfs-diag\ndfs-h\ndfs-diag-h\nbfs\nExit\nPlease enter the command:")
    if cmd.lower() == 'dfs':
        DFS(agent_coord)
    elif cmd.lower() == 'bfs':
        BFS(agent_coord)
    elif cmd.lower() == 'dfs-diag':
        DFS(agent_coord, adjacent_cells=adj_diag)
    elif cmd.lower() == 'dfs-h':
        DFS(agent_coord, heuristic=l2norm)
    elif cmd.lower() == 'dfs-diag-h':
        DFS(agent_coord, adjacent_cells=adj_diag, heuristic=l2norm)

    elif cmd.lower() == 'exit':
        break
    else:
        print('Command not found')
        continue
    input("Press enter to continue to the menu.")
