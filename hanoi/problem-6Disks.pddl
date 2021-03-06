
(define (problem 6Disks)
(:domain hanoi)
(:objects source auxillary destination d1 d2 d3 d4 d5 d6)
(:init

(smaller d1 source)
(smaller d2 source)
(smaller d3 source)
(smaller d4 source)
(smaller d5 source)
(smaller d6 source)
(smaller d1 auxillary)
(smaller d2 auxillary)
(smaller d3 auxillary)
(smaller d4 auxillary)
(smaller d5 auxillary)
(smaller d6 auxillary)
(smaller d1 destination)
(smaller d2 destination)
(smaller d3 destination)
(smaller d4 destination)
(smaller d5 destination)
(smaller d6 destination)

(smaller d2 d1)
(smaller d3 d2)
(smaller d3 d1)
(smaller d4 d1)
(smaller d4 d2)
(smaller d4 d3)
(smaller d5 d1)
(smaller d5 d2)
(smaller d5 d3)
(smaller d5 d4)
(smaller d6 d1)
(smaller d6 d2)
(smaller d6 d3)
(smaller d6 d4)
(smaller d6 d5)

(on d1 source)
(on d2 d1)
(on d3 d2)
(on d4 d3)
(on d5 d4)
(on d6 d5)

(clear d6)
(clear auxillary)
(clear destination)
)
(:goal
(and
(on d1 destination)
(on d2 d1)
(on d3 d2)
(on d4 d3)
(on d5 d4)
(on d6 d5)
)
)
)
