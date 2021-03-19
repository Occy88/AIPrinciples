import heapq
import math
import os
import random

from matplotlib import pyplot as plt

PRINT_VISITING = True
PRINT_PLAN = False
MOVE_NUMBER = 0


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Disk:
    """
    Represents a disk of size v
    """

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
    """
    Error for Empty peg
    """

    def __str__(self):
        print("Peg is empty")


class DiskTooBig(Exception):
    """
    Error for Disk placement on smaller disk
    """

    def __str__(self):
        print("disk on bottom must be larger or base than disk on top.")


class Peg:
    """
    Represents a Peg for towers of hanoi
    """

    def __init__(self, height, id=0):
        self.disks = []
        self.id = id
        # for variable height (future variation of problem)?
        self.h = height

    def top(self):
        """
        Returns top disk
        """
        try:
            return self.disks[-1]
        except IndexError:
            raise EmptyPeg

    def pop(self):
        """
        returns top disk and removes it
        """
        try:
            return self.disks.pop()
        except IndexError:
            raise EmptyPeg

    def put(self, disk: Disk):
        """
        places disk onto peg (must be smaller than current top).
        """
        if len(self) <= 0 or disk < self.top():
            self.disks.append(disk)
        else:
            raise DiskTooBig("Disk To Big: ", "top:", self.top(), " , placing:", disk)

    def __lt__(self, other):
        """
        Checks if value of peg is smaller than onother peg
        (if top disk is less than top of other)
        """
        try:
            return self.top() < other.top()
        except EmptyPeg:
            if len(self.disks) <= 0:
                return False
            return True

    def __gt__(self, other):
        """
        opposite of __lt__
        """
        try:
            # print('+++', self.top(), other.top())
            return self.top() > other.top()
        except EmptyPeg:
            if len(self.disks) <= 0:
                return True
            return False

    def __hash__(self):
        """
        Hash representation of peg (id and disks)
        """
        return hash((self.id, frozenset(self.disks)))

    def __eq__(self, other):
        """
        Test if two pegs are the same (id & disks)
        """
        return self.id == other.id and self.disks == other.disks

    def __mul__(self, other: int):
        """
        (generates multiple pegs with incremental id's for easy tower of hanoi instance
        initiation)
        """
        pegs = [self]
        for i in range(other - 1):
            pegs.append(Peg(self.h, self.id + i + 1))
        return pegs

    def __index__(self):
        return self.disks

    def __getitem__(self, item: int):
        return self.disks[item]

    def __len__(self):
        """
        returns num of disks
        """
        return len(self.disks)

    def __str__(self):
        """
        returns str representation
        """
        return str((self.id, self.disks))


class Domain:
    """
    A generic domain with a heuristic to
    evaluate it.
    """

    def __init__(self, domain, heuristic):

        self.domain = domain
        self.heuristic = heuristic

    def expand(self) -> set:
        """
        returns set of possible actions from a given state
        """
        pass

    def perform_action(self, action):
        """
        applies action to state
        """
        pass

    def __gt__(self, other):
        """
        checks if heuristic domain value against another
        """
        try:
            return self.heuristic(self) > self.heuristic(other)
        except Exception:
            raise Exception("No heuristic provided")

    def __lt__(self, other):
        """
        opposite of __gt__
        """
        try:
            return self.heuristic(self) < self.heuristic(other)
        except Exception:
            raise Exception("No heuristic provided")

    def __eq__(self, other):
        """
        tests if domain is equivalent to another
        """
        return self.__hash__() == hash(other)

    def __hash__(self):
        return hash(self.domain)


class Hanoi(Domain):
    """
    Hanoi Domain
    """

    def __init__(self, num_pegs, max_disks, heuristic):
        """
        domain is a set of pegs of a given height
        to which disks can be added
        """
        domain = Peg(max_disks) * num_pegs
        super(Hanoi, self).__init__(domain, heuristic)
        self.p = None
        self.p_action = None
        self.depth = 0

    def expand(self):
        """
        returns set of possible moves as
        [(from,to),...]
        """
        possible = set()
        for p1 in self:
            for p2 in self:
                if p1.id == p2.id or p1 > p2:
                    continue
                possible.add((p1.id, p2.id))
        return possible

    def perform_action(self, action: (int, int)):
        """
        performs and action:
         pop from one peg put on another
        """
        self[action[1]].put(self[action[0]].pop())

    def explore_action(self, action, heuristic) -> (int, int):
        """
        Explores an action (checks the value and hash of an action)
        without changing current domain.
        """
        # apply
        self.perform_action(*action)
        v, h = (heuristic(self), self.__hash__())
        # revert
        self.perform_action(*action[::-1])
        return v, h

    def print_ascii(self):
        """
        assumes pegs of all same height for now.
        h=4,
        ___=     l=1 p=3 v=1
        __===    l=3 p=2 v=2
        _=====   l=5 p=1 v=3
        =======  l=7 p=0 v=4
        p=h-b l=2v-1
        """
        m_h = self[0].h

        for h in range(m_h):
            i = m_h - h - 1
            for index, p in enumerate(self):
                try:
                    col = bcolors.OKBLUE
                    # print(m_h)
                    # print(i)
                    # time.sleep(1)
                    if (m_h - i) == p[i].v:
                        col = bcolors.OKGREEN
                    dl = 2 * p[i].v - 1
                    padding = m_h - p[i].v
                    print(' ' * padding, end='')
                    print(col, '=' * dl, bcolors.ENDC, end='')
                    print(' ' * padding, end='')
                except IndexError:
                    print(' ' * (m_h * 2 + 1), end='')
                print('||', end='')
            print('')

    @staticmethod
    def on_goal_and_incorrect(self):
        """
        THIS HEURISTIC ASSUES THAT ALL DISKS ARE PRESENT IN INCREMENTAL SIZE
        Simple heuristic (admissible)
        Assumes the target goal is all disks mounted on last peg.
        sum of:
        num disks not on goal peg (rationale: at least one move to get there for each disk)
        2 * num disks on goal peg of incorrect size (rationale: at least two moves (need to get out the way))

        """
        # number not on goal is height of goal peg - number on peg
        total_correct = 0
        total_incorrect = 0
        # assume that disks stacked incremental height on goal. [5,4,3,2,1,0]
        for i, d in enumerate(self[-1].disks):
            # print("disk v: ", d.v, ", self.h: ", self[-1].h)
            if d.v < self[-1].h - i:
                total_incorrect += 1
            else:
                total_correct += 1
        return (self[-1].h - total_correct) + 2 * total_incorrect

    @staticmethod
    def on_goal(self):
        # number not on goal is height of goal peg - number on peg
        total_correct = 0
        total_incorrect = 0
        # assume that disks stacked incremental height on goal. [5,4,3,2,1,0]
        for i, d in enumerate(self[-1].disks):
            # print("disk v: ", d.v, ", self.h: ", self[-1].h)
            if d.v < self[-1].h - i:
                total_incorrect += 1
            else:
                total_correct += 1
        # print(total_incorrect)
        return self[0].h - total_correct

    @staticmethod
    def random(self):
        return random.randint(1, 10)

    @staticmethod
    def blind(self):
        """
        My second admissible heuristic (blind heuristic)
        """
        return 0

    def print(self):
        """

        """
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

    def __len__(self):
        return len(self.domain)


import copy


# #
class Problem:

    def __init__(self, domain: Domain):
        self.expanded = set()
        self.visited = set()
        self.goal_state_hash = 0
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
            c.p_action = a
            c.depth = self.d.depth + 1
            c.perform_action(a)
            h = hash(c)
            if not (h == self.goal_state_hash) and (h in self.expanded or h in self.visited):
                continue
            heapq.heappush(heap, c)
            self.expanded.add(h)
        return heap

    def a_star(self, optimal=False, timeout=100 * 60, as_bfs=False):
        """
        as_bfs = True expand all nodes before searching next nodes (still ordered by heuristic)
        as_bfs = False expand current node and push the expansion onto min heap, (may give sub-optimal result)
        a_star : will not find optimal path if heuristic is not consistent, (consistent includes current cost/depth)
        only admissible ones. (consistent would include current depth.)
        optimal = False/True, will keep looking for better path until exhaustion
        optimal does not provide an optimal path with as_bfs=False if heuristic is inconsistent.
        timeout= timeout for search.

        """
        t = time.time()
        global MOVE_NUMBER, PRINT_VISITING
        MOVE_NUMBER += 1
        to_eval = self.expand([])
        self.visited.add(hash(self.d))
        min_length = math.inf
        min_plan = []
        min_actions = []
        temp_heap = []
        while len(to_eval) > 0:
            state = heapq.heappop(to_eval)
            self.d = state
            if PRINT_VISITING:
                self.d.print_ascii()
                clear()
            MOVE_NUMBER += 1
            h = hash(state)
            self.visited.add(hash(state))
            plan = []
            actions = []
            if h == self.goal_state_hash:
                print("========= GOAL FOUND ============")
                while self.d.p is not None:
                    plan.append(copy.deepcopy(self.d))
                    actions.append(self.d.p_action)
                    self.d = self.d.p
                if optimal:
                    if len(plan) < min_length:
                        min_plan = plan
                        min_actions = actions
                        min_length = len(plan)
                else:
                    return plan, actions
            # self.print()
            # expand only if we are not on goal state, as it makes not sense to keep searching after goal has been found
            # goal may be sub-optimal and we may be looking for optimal goal, hence keep searching...
            # :D

            if as_bfs:
                if not (h == self.goal_state_hash):
                    temp_heap = self.expand(temp_heap)
                #     replace to eval with the expansion (temp_heap)
                #  if it has been exhausted (bfs)
                if len(to_eval) == 0:
                    to_eval = temp_heap
                    temp_heap = []
            else:
                if not (h == self.goal_state_hash):
                    to_eval = self.expand(to_eval)
            if time.time() - t > timeout:
                print("timeout")
                return [], []
            # print(to_eval)
        print("SPACE EXHAUSTED")
        return min_plan, min_actions


import time
from os import system, name


# import sleep to show output for some time period


# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def stack_disks(peg, num_disks):
    for i in range(num_disks):
        peg.put(Disk(num_disks - i))


def find_max_m(timeout):
    for n in range(1, 1000):
        print("------------[ ", n, ' ]------------------')
        d = Hanoi(3, n, Hanoi.blind)
        stack_disks(d[0], n)
        g = Hanoi(3, n, None)
        stack_disks(g[-1], n)
        p = Problem(d)
        p.goal_state_hash = hash(g)
        plan, actions = p.a_star(True, timeout)
        print(len(plan))
        if len(plan) > 0:
            continue
        else:
            return n


def main(*args, **kwargs):
    global MOVE_NUMBER
    global PRINT_VISITING
    global PRINT_PLAN
    # keeps searching until exhaustion, selects shortest found (builds the pdb fully)
    optimal = True
    # uses bfs (otherwise a*) note - heuristic must be consistent for optimal solution
    as_bfs = True
    max_time = 10 * 60
    if not os.path.exists('plans'):
        os.makedirs('plans')
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    # change print visiting to true if you would like to see
    # what states are being visited.
    times = {}
    # test each heuristic.
    for ind, h in enumerate((Hanoi.random, Hanoi.blind, Hanoi.on_goal, Hanoi.on_goal_and_incorrect)):
        times[h.__name__] = []
        # number of disks from:to-1
        for n in range(1, 1000):
            time.sleep(1)
            print("EVALUATING: ", h.__name__)

            print("tower height: ", n)
            MOVE_NUMBER = 0
            t = time.time()
            d = Hanoi(3, n, h)
            stack_disks(d[0], n)
            g = Hanoi(3, n, None)
            stack_disks(g[-1], n)
            p = Problem(d)
            p.goal_state_hash = hash(g)
            # plan is each instance of the domain,
            # actions are the actions between domains, (also included in domain)
            # but I separated them so ease (see a_star goal condition reached recovery...)

            plan, actions = p.a_star(optimal=optimal, timeout=max_time, as_bfs=as_bfs)
            # implies timout hence break as max n reached...
            if len(plan) <= 0:
                print("N -(timeout) :", n)
                break
            time_to_completion = time.time() - t
            print("PLAN LENGTH: ", len(plan))
            print("Now showing plan:")
            # to print out each state in the plan (visual.
            # time.sleep(2)
            if PRINT_PLAN:
                for d in plan:
                    d.print_ascii()
                    clear()
            #  save plan to file.
            f = open('plans/' + h.__name__ + ' d:' + str(n), 'w')
            actions.reverse()

            # SAVE PLAN (ACTIONS)
            for a in actions:
                f.write(str(a) + '\n')
            f.close()
            times[h.__name__].append((MOVE_NUMBER, len(plan), time_to_completion))
            print("________________[ ", n, " ]____________________")

    # SAVE RESULTS
    for key, val in times.items():
        print(key)
        print('visited | plan_length | time(s)', )
        x_vals = []
        y_vals = []
        i = 0
        for nmoves, plen, t in val:
            i += 1
            x_vals.append(t)
            y_vals.append(i)
            print(nmoves, '|', plen, '|', t)
        # x_vals.reverse()
        print(x_vals)
        print(y_vals)
        plt.plot(y_vals, x_vals, label=key)
        plt.ylabel('time')
        plt.xlabel('num disks')
        plt.title('optimal: ' + str(optimal) + 'heuristic: ' + key)
        plt.legend()
        plt.savefig('graphs/' + key + '.png')
        print("-------------------------------")
        print("FOR FIGURES SEE graphs/")
        print("FOR PLANS SEE plans/")


if __name__ == '__main__':
    # print(find_max_m(5 * 60))
    main()
