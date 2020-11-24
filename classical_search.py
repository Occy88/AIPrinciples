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

print_rate_per_sec = 0.2
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


def print_map():
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in current_map:
        s1 = ''
        for item in row:
            if item == WALL_SYMBOL:
                format = ';'.join([str(1), str(30)])
                s1 += u'\x1b[%sm \u25A8\x1b[0m' % (format)
            elif item == EXPANDED_NOT_VISITED_CELL_SYMBOL:
                format = ';'.join([str(1), str(33)])
                s1 += u'\x1b[%sm \u25CF\x1b[0m' % (format)
            elif item == VISITED_CELL_SYMBOL:
                format = ';'.join([str(1), str(31)])
                s1 += u'\x1b[%sm \u25CF\x1b[0m' % (format)
            else:
                format = ';'.join([str(1), str(30)])
                s1 += u'\x1b[%sm %s\x1b[0m' % (format, item)
        print(s1)


def valid_cell(row, col):
    return row >= 0 and row < len(current_map) and col >= 0 and col < len(current_map[0]) and current_map[row][
        col] is not WALL_SYMBOL and current_map[row][col] is not VISITED_CELL_SYMBOL


# ASSUMING POS+[COL,ROW]: column is right left, row is up down

L, LU, U, RU, R, RD, D, LD = [-1, 0], [-1, 1], [0, 1], [0, 1], [1, 0], [1, -1], [0, -1], [-1, -1]
adj = (L, U, R, D)
diag = (LU, RU, RD, LD)
adj_diag = adj + diag


# can't use numpy so a couple extra function to make life easier:
def s(p1, p2):
    return [p1[0] + p2[0], p1[1] + p2[1]]


def generate_adjacent_cells(y: int, x: int, cells=adj):
    return list(s(cell, [y, x]) for cell in cells if valid_cell(*s(cell, [y, x])))


def BFS(y, x):
    q = queue.Queue()
    q.put([y, x])
    while not q.empty():
        potential = q.get()
        if goal_coord == potential:
            current_map[potential[0]][potential[1]] = AGENT_SYMBOL
            print_map()
            return True
        current_map[potential[0]][potential[1]] = VISITED_CELL_SYMBOL
        expand = generate_adjacent_cells(*potential)
        list = [q.put(cell) for cell in expand]
        for cell in expand:
            current_map[cell[0]][cell[1]] = EXPANDED_NOT_VISITED_CELL_SYMBOL
        print_map()
        time.sleep(print_rate_per_sec)

    return False


def DFS(agent_row, agent_col):
    # Check if the current state is goal state
    if agent_row == goal_coord[0] and agent_col == goal_coord[1]:
        print_map()
        return True

    # Calculate the position of agent adjacent cells for exploration
    # quick transpose as I prefer the generate adjacent cells function remains how it is (list of coords)
    adjacent_cells = list(map(list, zip(*generate_adjacent_cells(agent_row, agent_col))))
    if len(adjacent_cells) == 0:
        return False
    adjacent_cells_row = adjacent_cells[0]
    adjacent_cells_col = adjacent_cells[1]

    # Set the status of adjacent cells of agent to expanded and not visited
    for i in range(len(adjacent_cells_row)):
        if valid_cell(adjacent_cells_row[i], adjacent_cells_col[i]):
            current_map[adjacent_cells_row[i]][adjacent_cells_col[i]] = EXPANDED_NOT_VISITED_CELL_SYMBOL

    print_map()
    time.sleep(print_rate_per_sec)

    # Set the status of current agent cell to visited
    current_map[agent_row][agent_col] = VISITED_CELL_SYMBOL
    for i in range(len(adjacent_cells_row)):
        # Check if the adjacent cell is not visited before and not wall
        if valid_cell(adjacent_cells_row[i], adjacent_cells_col[i]):
            # Move the agent to the new adjacent cell and change its status
            current_map[adjacent_cells_row[i]][adjacent_cells_col[i]] = AGENT_SYMBOL
            # Run DFS for the new state recursively
            res = DFS(adjacent_cells_row[i], adjacent_cells_col[i])
            if res == True:
                return res

    return False


while True:
    current_map = deepcopy(initial_map)
    print_map()
    cmd = input("Commands:\nDFS\nBFS\nExit\nPlease enter the command:")
    if cmd.lower() == 'dfs':
        DFS(agent_coord[0], agent_coord[1])
    elif cmd.lower() == 'bfs':
        BFS(agent_coord[0], agent_coord[1])
    elif cmd.lower() == 'exit':
        break
    else:
        print('Command not found')
        continue
    input("Press enter to continue to the menu.")
