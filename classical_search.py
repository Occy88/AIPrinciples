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

print_rate_per_sec = 1.0
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

L, LU, U, RU, R, RD, D, LD = [-1, 0], [-1, 1], [0, 1], [0, 1], [1, 0], [1,-1], [-1, -1], [-1, -1]

# can't use numpy so a couple extra function to make life easier:
def s(p1, p2):
    return [p1[0] + p2[0], p1[1] + p2[1]]


def generate_adjacent_cells(y: int, x: int, diag=False):
    # agent_row is the row where currently the agent is
    # agent_col is the column where currently the agent is
    l = [[-1, 0], [1, 0], [0, 1], [0, -1], [1, -1], [1, 1], [-1, 1], [-1, -1]]
    # Calculate the position of adjacent cells around the agent for later exploration by DFS or BFS.
    # left_of_agent_row= agent_row
    # left_of_agent_col = agent_col -1
    # ...
    # ...

    # diagonal move support
    # ...
    # ...

    # Defining the order of adjacent cells expanding by the agent for BFS and DFS algorithms.
    # Use "append" method. i.e. adjacent_cells_row.append(left_of_agent_row)
    adjacent_cells_row = []
    adjacent_cells_col = []

    # adjacent_cells_row.append(...)
    # adjacent_cells_col.append(...)

    return [adjacent_cells_row, adjacent_cells_col]  # returning the list of genereted adjacent cells for DFS and BFS


def BFS(agent_start_row, agent_start_col):
    # Add the initial position of the agent to queue
    Q = queue.Queue()
    Q.put([agent_start_row, agent_start_col])

    while not Q.empty():
        Q.
        pass

    # Retrieve the head of queue as the next position of the agent to explore

    # Set the status of the cell as the agent is there

    # Check whether the agent has found the goal

    # Calculate the position of agent adjacent cells for exploration

    # check if the adjacent cells are valid (not wall and not visited before) and add them to the queue for further search

    # Set the current status of the agent cell to visited

    return False


def DFS(agent_row, agent_col):
    # Check if the current state is goal state
    if agent_row == goal_coord[0] and agent_col == goal_coord[1]:
        print_map()
        return True

    # Calculate the position of agent adjacent cells for exploration
    adjacent_cells = generate_adjacent_cells(agent_row, agent_col)
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
