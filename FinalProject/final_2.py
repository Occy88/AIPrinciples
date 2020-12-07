MOVE_NUMBER = 0
import heapq


# Problem representation
# p[m][n]=k
# where k is the size of the peg
# p = nxm array
# where n is number of pegs
# m  is number of spaces available -1 (to store index next free space)
# this is because there is only one spot where disk can be placed
#  on any peg, hence storing it makes it faster.
class Disk:
    def __init__(self, size=1):
        self.v = size

    def __lt__(self, other):
        return self.v < other.v

    def __gt__(self, other):
        return self.v > other.v

    def __hash__(self):
        return self.v

    def __str__(self):
        return str(self.v)


class EmptyPeg(Exception):
    def __str__(self):
        print("Peg is empty")


class DiskTooBig(Exception):
    def __str__(self):
        print("disk on bottom must be larger or base than disk on top.")


class Peg:
    def __init__(self, height, id=0):
        self.disks = []
        self.id = id
        # for variable height?
        self.h = height

    def top(self):
        try:
            return self.disks[-1]
        except IndexError:
            raise EmptyPeg

    def pop(self):
        try:
            return self.disks.pop()
        except IndexError:
            raise EmptyPeg

    def put(self, disk: Disk):
        if len(self) <= 0 or disk < self.top():
            self.disks.append(disk)
        else:
            raise DiskTooBig("Disk To Big: ", "top:", self.top(), " , placing:", disk)

    def __lt__(self, other):
        try:
            return self.top() < other.top()
        except EmptyPeg:
            if len(self.disks) <= 0:
                return False
            return True

    def __gt__(self, other):
        try:
            # print('+++', self.top(), other.top())
            return self.top() > other.top()
        except EmptyPeg:
            if len(self.disks) <= 0:
                return True
            return False

    def __hash__(self):
        return hash((self.id, frozenset(self.disks)))

    def __eq__(self, other):
        return self.id == other.id and self.disks == other.disks

    def __mul__(self, other: int):
        pegs = [self]
        for i in range(other - 1):
            pegs.append(Peg(self.h, self.id + i + 1))
        return pegs

    def __index__(self):
        return self.disks

    def __len__(self):
        return len(self.disks)

    def __str__(self):
        return str((self.id, self.disks))


class Domain:
    def __init__(self, domain, heuristic):
        self.domain = domain
        self.heuristic = heuristic

    def expand(self) -> set:
        pass

    def perform_action(self, action):
        """
        applies action
        """
        pass

    def __gt__(self, other):
        try:
            return self.heuristic(self.domain) > self.heuristic(other.domain)
        except Exception:
            raise Exception("No heuristic provided")

    def __lt__(self, other):
        try:
            return self.heuristic(self.domain) < self.heuristic(other.domain)
        except Exception:
            raise Exception("No heuristic provided")

    def __eq__(self, other):
        return self.__hash__() == hash(other)

    def __hash__(self):
        return hash(self.domain)


class Hanoi(Domain):
    def __init__(self, num_pegs, max_disks, heuristic):
        domain = Peg(max_disks) * num_pegs
        super(Hanoi, self).__init__(domain, heuristic)
        self.p = None

    def expand(self):
        possible = set()
        for p1 in self:
            for p2 in self:
                if p1.id == p2.id or p1 > p2:
                    continue
                # print('----------')
                # print(p1 == p2)
                # print(p1 > p2)
                # print(p1 < p2)
                # print(p1, p2)
                # print('____________')
                possible.add((p1.id, p2.id))
        return possible

    def perform_action(self, action: (int, int)):
        self[action[1]].put(self[action[0]].pop())

    def explore_action(self, action, heuristic) -> (int, int):
        # apply
        self.perform_action(*action)
        v, h = (heuristic(self), self.__hash__())
        # revert
        self.perform_action(*action[::-1])
        return v, h

    @staticmethod
    def heuristic_1(self):
        """
        Simple heuristic (admissible)
        Assumes the target goal is all disks mounted on last peg.
        sum of:
        num disks not on goal peg (rationale: at least one move to get there for each disk)
        2 * num disks on goal peg of incorrect size (rationale: at least two moves (need to get out the way))

        """
        # number not on goal is height of goal peg - number on peg
        # print(self)
        # print(self[-1])
        # print("----------heuristic=------")
        num_not_on_goal = self[-1].h - len(self[-1])
        # print("not on goal: ", num_not_on_goal)
        total_incorrect = 0
        # assume that disks stacked incremental height on goal. [5,4,3,2,1,0]
        for i, d in enumerate(self[-1].disks):
            # print("disk v: ", d.v, ", self.h: ", self[-1].h)
            if d.v < self[-1].h - i:
                total_incorrect += 1
        # print(total_incorrect)
        return num_not_on_goal + 2 * total_incorrect

    def print(self):
        for p in self.domain:
            print(len(p), end=' ')

    def __getitem__(self, item) -> Peg:
        return self.domain[item]

    def __hash__(self):
        return hash(frozenset(self.domain))

    def __deepcopy__(self, memo):
        # create a copy with self.linked_to *not copied*, just referenced.
        c = Hanoi(0, 0, self.heuristic)
        c.domain = copy.deepcopy(self.domain)
        return c


import copy


# #
class Problem:
    expanded = set()
    visited = set()
    goal_state_hash = 0

    def __init__(self, domain: Domain):
        self.d = domain

    def set_goal_state_hash(self, goal_hash):
        self.goal_state_hash = goal_hash

    def expand(self, heap):
        actions = self.d.expand()
        # remove states created by moves that are in explored or visited
        # print("=======actions=========", actions)
        for a in actions:
            c = copy.deepcopy(self.d)
            c.p = self.d
            c.perform_action(a)
            h = hash(c)
            if h in self.expanded or h in self.visited:
                continue
            heapq.heappush(heap, c)
            self.expanded.add(h)
        return heap

    def a_star(self):
        global MOVE_NUMBER
        MOVE_NUMBER += 1
        to_eval = self.expand([])
        self.visited.add(hash(self.d))
        # self.d.print()
        print(self.goal_state_hash)
        print(to_eval)

        while len(to_eval) > 0:
            state = heapq.heappop(to_eval)
            self.d = state
            # self.d.print()
            MOVE_NUMBER += 1
            h = hash(state)
            self.visited.add(hash(state))
            if h == self.goal_state_hash:
                print("========= GOAL FOUND ============")
                print("======= RECOVERING PLAN ============")
                l = 1
                while self.d.p is not None:
                    l += 1
                    self.d.print()
                    self.d = self.d.p
                    print('---')
                self.d.print()
                print("\nPLAN LEN: ", l)
                print("MOVES: ", MOVE_NUMBER)
                return True
            # self.print()
            to_eval = self.expand(to_eval)
            # print(to_eval)
        print("GOAL NOT FOUND")
        return False


import time

t = time.time()
n = 10
d = Hanoi(3, n, Hanoi.heuristic_1)
print("=================")
print(d[-1])
for i in range(n):
    d[0].put(Disk(n - i))
g = Hanoi(3, n, None)
for i in range(n):
    g[-1].put(Disk(n - i))
p = Problem(d)
p.goal_state_hash = hash(g)
p.a_star()
print(time.time() - t)
