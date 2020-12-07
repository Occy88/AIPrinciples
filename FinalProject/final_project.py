MOVE_NUMBER = 0
import heapq
import queue
import numpy as np
# Problem representation
# p[m][n]=k
# where k is the size of the peg
# p = nxm array
# where n is number of pegs
# m  is number of spaces available -1 (to store index next free space)
# this is because there is only one spot where disk can be placed
#  on any peg, hence storing it makes it faster.

class Hanoi:
    p = np.array([])
    # a set of states and values
    # state is presented as: (hash, val)
    expanded = set()
    visited = set()
    goal_state_hash = 0

    def __init__(self, pegs, disks):
        self.pegs = pegs
        self.disks = disks

    def set_goal_state_hash(self, goal_hash):
        self.goal_state_hash = goal_hash

    def heuristic(self):
        """
        Simple heuristic (admissible)
        sum of:
        num disks not on goal peg (rationale: at least one move to get there for each disk)
        2 * num disks not on goal peg larger than top of goal peg (rationale: at least two moves (need to get out the way))
        """
        num_not_on_goal = 1 + self.disks - self.nf(self.pegs - 1)
        if self.val(self.pegs - 1) > 0:
            # 2*(disks-val-(index-1) )
            disk_size = self.val(self.pegs - 1)
            disk_index = self.nf(self.pegs - 1) - 1
            larger_than = 2 * (self.disks - disk_size - disk_index)
        else:
            larger_than = 0
        if self.__hash__() == self.goal_state_hash:
            print(num_not_on_goal, larger_than)
        # self.print()
        return num_not_on_goal + larger_than

    def expand(self):
        moves = self.generate_moves()
        # remove states created by moves that are in explored or visited
        states_sorted = []
        for m in moves:
            state, p = self.next_state_hash_val(m)
            if state in self.expanded or state in self.visited:
                continue
            heapq.heappush(states_sorted, (state, p))
            self.expanded.add(state)
        return [heapq._heappop_max(states_sorted) for i in range(len(states_sorted))]

    def dfs(self):
        global MOVE_NUMBER
        MOVE_NUMBER += 1
        to_eval = queue.Queue()
        for s in self.expand():
            to_eval.put(s)

        self.visited.add((self.heuristic(), self.__hash__()))

        while not to_eval.empty():
            state, p = to_eval.get()
            MOVE_NUMBER+=1
            self.p = p
            self.visited.add(state)
            if state[1] == self.goal_state_hash:
                print("========= GOAL FOUND ============")
                print("MOVES: ", MOVE_NUMBER)
                self.print()
                return True
            # self.print()
            for s in self.expand():
                to_eval.put(s)
        return False

    def reset(self, peg):
        """
        Resets the problem, all pegs stacked on first index, largest to smallest.
        """
        self.p = np.zeros(shape=(self.disks + 1, self.pegs), dtype=np.uint8)
        # initiate values the next free index
        for i in range(0, self.pegs):
            self.p[0][i] = 1

        # initiate all disks to first peg (starting with largest.
        for i in range(0, self.disks):
            self.place_disk(self.disks - i, peg)

    def place_disk(self, disk, peg):
        """
        Sets the next free index of the peg to the value of the disk
        increments value next free index by 1.
        """
        self.p[self.nf(peg)][peg] = disk
        self.p[0][peg] += 1

    def remove_disk(self, peg):
        """
        returns value of disk removed
        """
        disk = self.val(peg)
        self.p[self.nf(peg) - 1][peg] = 0
        self.p[0][peg] -= 1
        return disk

    def val(self, peg):
        """
        Returns value of top disk on a peg
        """
        nf = self.nf(peg)
        if nf == 1:
            return 0
        return self.p[self.nf(peg) - 1][peg]

    def nf(self, peg):
        """
        Returns index of next free index on a peg
        """
        return self.p[0][peg]

    def can_move(self, peg_from, peg_to):
        return self.nf(peg_to) == 1 or self.val(peg_from) < self.val(peg_to)

    def generate_moves(self):
        """
        returns tuples of next possible moves
        Possible moves are defined by properties:
        peg not empty,
1997
        for disk on peg (top one)
            for disk on other pegs:
                check if move possible.
        """
        moves = []
        for peg in range(self.pegs):
            val = self.val(peg)
            if val == 0:
                continue
            for other_p in range(self.pegs):
                if other_p == peg:
                    continue
                if self.can_move(peg, other_p):
                    moves.append((peg, other_p))
        return moves

    def next_state_hash_val(self, move):
        self.move(*move)
        h = self.__hash__()
        val = self.heuristic()
        p = np.copy(self.p)
        self.move(*np.flip(move))
        return (val, h), p

    def move(self, peg_from, peg_to):
        # preconditions:
        # size from < size to or to==base.
        self.place_disk(self.remove_disk(peg_from), peg_to)

    def print_disk(self, disk_val):
        disk_char = '='
        num_chars = disk_val * 2 - 1
        total_chars = self.disks * 2 - 1
        free_spots = int((total_chars - num_chars) / 2)
        if num_chars <= 0:
            free_spots -= 1
            print(" ", end='')

        # print(disk_val, num_chars, total_chars, free_spots)

        print(' ' * free_spots, end='')
        print(disk_char * num_chars, end='')
        print(' ' * free_spots, end='|')

    def print(self):
        global MOVE_NUMBER
        clear()

        for h in range(1, self.disks + 1):
            for peg in range(self.pegs):
                self.print_disk(self.p[self.disks + 1 - h][peg])
            print('')
        print("")
        print("Move number: ", MOVE_NUMBER)
        time.sleep(0.2)

    def print_move(self, move):
        self.move(*move)
        print("=======MOVE: ", move, "==========")
        print("HASH: ", self.__hash__())
        print("VAL: ", self.heuristic())

        self.print()
        self.move(*np.flip(move))

    def __hash__(self):
        return hash(str(self.p))


from os import system, name


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

import time
p = Hanoi(3, 9)
p.reset(0)
print("STARTING STATE: ")
p.print()
print("GOAL STATE: ")
g = Hanoi(3, 9)
g.reset(2)
g.print()

p.set_goal_state_hash(g.__hash__())
t = time.time()
print(p.dfs())
print(time.time() - t)
