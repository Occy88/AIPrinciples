MOVE_NUMBER = 0
import heapq


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
            for p in self:
                try:
                    dl = 2 * p[i].v - 1
                    padding = m_h - p[i].v
                    print(' ' * padding, end='')
                    print('=' * dl, end='')
                    print(' ' * padding, end='')
                except IndexError:
                    print(' ' * (m_h * 2 - 1), end='')
                print('', end='||')
            print('')


    @staticmethod
    def heuristic_on_goal(self):
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
        return self[-1].h - total_correct

    def heuristic_blind(self):
        """
        My second admissible heuristic (blind heuristic)
        """
        return 0
        pass

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
        while len(to_eval) > 0:
            state = heapq.heappop(to_eval)
            # state.print_ascii()
            # print(state.heuristic(state))
            self.d = state
            # self.d.print()
            MOVE_NUMBER += 1
            h = hash(state)
            self.visited.add(hash(state))
            plan = []
            if h == self.goal_state_hash:
                print("========= GOAL FOUND ============")
                while self.d.p is not None:
                    plan.append(copy.deepcopy(self.d))
                    self.d = self.d.p
                return plan
            # self.print()
            to_eval = self.expand(to_eval)
            # print(to_eval)
        print("GOAL NOT FOUND")
        return []


import time


def main():
    global MOVE_NUMBER
    times = {}
    # n = 3
    # h = Hanoi.heuristic_1
    # d = Hanoi(n, 4, h)
    # d[2].put(Disk(4))
    # d[2].put(Disk(3))
    # d[2].put(Disk(2))
    # d[0].put(Disk(1))
    # actions = d.expand()
    # for a in actions:
    #     c = copy.deepcopy(d)
    #     c.perform_action(a)
    #     c.print_ascii()
    #     print(c.heuristic(c))
    #
    # p = Problem(d)
    # print("____________________________________")
    # st = p.expand([])
    # for c in st:
    #     c.print_ascii()
    # heapq.heappop(st).print_ascii()
    # exit(0)
    for ind, h in enumerate(( Hanoi.heuristic_blind, Hanoi.heuristic_on_goal)):
        times[h.__name__] = []
        for n in range(2, 13):
            MOVE_NUMBER = 0
            # print("HEURISTIC: ", h.__name__)
            t = time.time()
            d = Hanoi(3, n, h)
            for i in range(n):
                d[0].put(Disk(n - i))
            # print("STATE: ")
            # d.print_ascii()
            g = Hanoi(3, n, None)
            for i in range(n):
                g[-1].put(Disk(n - i))
            # print("GOAL: ")
            # g.print_ascii()
            p = Problem(d)
            p.goal_state_hash = hash(g)
            # print(p.visited)
            # print(p.expanded)
            plan = p.a_star()
            print("PLAN LENGTH: ", len(plan))
            # for d in plan:
            #     d.print_ascii()
            times[h.__name__].append((MOVE_NUMBER, len(plan), time.time() - t))
            print("________________[ ", n, " ]____________________")
    for key, val in times.items():
        print(key)
        for nmoves, plen, t in val:
            print(nmoves, '|', plen, '|', t)
        print("-------------------------------")


if __name__ == '__main__':
    main()
