#!/usr/bin/env python
# coding: utf-8

# # CS5960-Octavio-delSer-100873054-lab2.ipynb

# Quick Summary:
# 
# ============= EXPANSION COUNTS ===============
# 
# DFS Adjacent cells No Heuristic:                         27 
# 
# DFS Adjacent and Diagonal cells No Heuristics:           29 
# 
# DFS Adjancent cells with L2 Heuristic:                   8
# 
# DFS Adjacent and Diagonal cells with L2 Heuristic:       6
# 
# BFS Adjacent cells:                                      18
# 
# BFS Adjacent and Diagonal cells:                         15
# 
# 
# 
# Notes: 
# 
# Code is written in python, in a Jupyter notebook for presentability.
# 
# I changed the print function so Latex would support generation of pdf
# 
# I changed the some code to support easier manipulation ov variables.
# 
# 

# ### Imports

# In[1]:


import math
import os
import queue
import time
from copy import deepcopy


# ### Statics:

# In[2]:


EXPANSION_COUNTER=0
AGENT_SYMBOL = 'A'
GOAL_SYMBOL = 'G'
WALL_SYMBOL = '#'
VISITED_CELL_SYMBOL = 'V'
EXPANDED_NOT_VISITED_CELL_SYMBOL = 'E'
EMPTY_SYMBOL = ' '
print_rate_per_sec = 0.01
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


# ### Defining cells that can be explored:
# As a sum of pos + cell
# L= left
# R= Right
# U= up
# D= down

# In[3]:


L, LU, U, RU, R, RD, D, LD = [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1]
adj = (L, U, R, D)
diag = (LU, RU, RD, LD)
adj_diag = adj + diag


# ### Map Printing

# In[4]:


def print_map():
    print("------EXPANSION: ",EXPANSION_COUNTER, "-------------")
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in current_map:
        print(' '.join(row))
    print("---------------------------------------")
    time.sleep(print_rate_per_sec)


# ### Valid cell definition:
# I Adjusted this to not include expanded cells
# as that sould be invalid, we already have them so ignore them.

# In[5]:


def valid_cell(row, col):
    return row >= 0 and row < len(current_map) and col >= 0 and col < len(current_map[0]) and current_map[row][
        col] is not WALL_SYMBOL and current_map[row][col] is not VISITED_CELL_SYMBOL and current_map[row][col] is not EXPANDED_NOT_VISITED_CELL_SYMBOL


# ### Sum of two vectors
# (assuming dimention 2)

# In[6]:


def s(p1, p2):
    return [p1[0] + p2[0], p1[1] + p2[1]]


# ### Generating adjacent valid cells to point
# takes an array of cells to be summed to point
# this way we can feely define what adjacent means.

# In[7]:


def generate_adjacent_cells(point, cells=adj):
    return list(s(cell, point) for cell in cells if valid_cell(*s(cell, point)))


# ### L2 norm for heuristic function...

# In[8]:


def l2norm(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# ### Ordering a set of points by a given heuristic and a goal.
# for example, closest point to goal using l2norm defined above,
# this can be expanded for any heuristic and dimension.
# again apologies for the difficult to read code as I did not use numpy.

# In[9]:


def order_by_heuristic(points, goal, func=l2norm):
    """
    returns the points sorted by the heuristic function and goal
    the order of points that best match the function.
    """
    scores = [func(*point, *goal) for point in points]
    sorted_indices = sorted(range(len(scores)), key=lambda k: scores[k])
    return list(map(lambda k: points[k], sorted_indices))


# ## BFS Implementation
# takes adjacent cells that we want to explore given a point.
# Code is pretty self explanatory with provided names,
# hence I left it without comments
# as it would only make it more unreadable.

# In[10]:


def BFS(point, adjacent_cells=adj):
    global EXPANSION_COUNTER
    q = queue.Queue()
    q.put(point)
    
    # Run untill empty queue
    while not q.empty():
        current = q.get()
        current_map[current[0]][current[1]] = AGENT_SYMBOL
        if goal_coord == current:
            print_map()
            print("GOAL FOUND")
            return True
        #Expand current
        expand = generate_adjacent_cells(current, cells=adjacent_cells)
        #Add all expanded cells to queue Could add a heuristic, but would not make
        # Sence unless branching factor is insanely large and depth 1 :D
        list = [q.put(cell) for cell in expand]
        #Check if there are any valid cells in expansion attempt to increment the counter.
        if len(expand)>0:
            EXPANSION_COUNTER+=1
        # Mark cells as Expande
        for cell in expand:
            current_map[cell[0]][cell[1]] = EXPANDED_NOT_VISITED_CELL_SYMBOL
        print_map()
        #Mark current cell as visited.
        current_map[current[0]][current[1]] = VISITED_CELL_SYMBOL
    return False


# ## DFS Implementation
# I slightly modified the implementation of DFS
# so that it is clearer.
# DFS unlike BFS contains a heuristic for which points to explore next
# as well as the adjacent cells to explore at any given point.

# In[11]:


def DFS(agent_coord, heuristic=None, adjacent_cells=adj):
    """+=
    heuristic: function by which to sort points (order of exploration)
    y,x: point where to start
    cells: which cells to expand list of vectors to som onto point (y,x)+cell -> (y',x')
    """
    # increment counter.
    global EXPANSION_COUNTER
    EXPANSION_COUNTER+=1
    # set agent coord to agent coord
    current_map[agent_coord[0]][agent_coord[1]] = AGENT_SYMBOL
    # set agent coord cell to visited

    # Check if the current state is goal state
    if agent_coord == goal_coord:
        print_map()
        print("GOAL FOUND")
        return True
    # get adjacent valid cells
    cells = generate_adjacent_cells(agent_coord, cells=adjacent_cells)
    if len(cells) <= 0:
        print_map()
        current_map[agent_coord[0]][agent_coord[1]] = VISITED_CELL_SYMBOL
        return False

    # check if heuristic is mentioned
    if heuristic is not None:
        cells = order_by_heuristic(cells, goal_coord, heuristic)
    
    # Mark cells as expanded
    for cell in cells:
        current_map[cell[0]][cell[1]] = EXPANDED_NOT_VISITED_CELL_SYMBOL
    print_map()
    current_map[agent_coord[0]][agent_coord[1]] = VISITED_CELL_SYMBOL

    # call dfs on all cells to visit in order.
    for cell in cells:
        if DFS(cell, heuristic=heuristic, adjacent_cells=adjacent_cells):
            return True
    return False


# ## RUN DFS - Adj only, No heuristic

# In[12]:


EXPANSION_COUNTER=0
current_map = deepcopy(initial_map)
print_map()
DFS(agent_coord)
print("EXPANSIONS: ",EXPANSION_COUNTER)


# ## RUN DFS - Adj and Diag, No Heuristic

# In[13]:


EXPANSION_COUNTER=0

current_map = deepcopy(initial_map)
print_map()
DFS(agent_coord, adjacent_cells=adj_diag)
print("EXPANSIONS: ",EXPANSION_COUNTER)


# ## RUN DFS - Adj only, With l2norm Heuristic

# In[14]:


EXPANSION_COUNTER=0

current_map = deepcopy(initial_map)
print_map()
DFS(agent_coord, heuristic=l2norm)
print("EXPANSIONS: ",EXPANSION_COUNTER)


# ## RUN DFS - Adj and Diag, With l2norm Heuristic

# In[15]:


EXPANSION_COUNTER=0

current_map = deepcopy(initial_map)
print_map()
DFS(agent_coord, adjacent_cells=adj_diag, heuristic=l2norm)
print("EXPANSIONS: ",EXPANSION_COUNTER)


# ## RUN BFS - Adj Only

# In[16]:


EXPANSION_COUNTER=0

current_map = deepcopy(initial_map)
print_map()
BFS(agent_coord)
print("EXPANSIONS: ",EXPANSION_COUNTER)


# ## RUN BFS - Adj And Diag

# In[17]:


EXPANSION_COUNTER=0
current_map = deepcopy(initial_map)
print_map()
BFS(agent_coord,adjacent_cells=adj_diag)
print("EXPANSIONS: ",EXPANSION_COUNTER)


# 
# 
