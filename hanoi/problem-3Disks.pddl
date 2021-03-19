

(define (problem 3Disks)
(:domain hanoi)
(:objects source auxillary destination d1 d2 d3)
(:init

(smaller d1 source)
(smaller d2 source)
(smaller d3 source)
(smaller d1 auxillary)
(smaller d2 auxillary)
(smaller d3 auxillary)
(smaller d1 destination)
(smaller d2 destination)
(smaller d3 destination)

(smaller d2 d1)
(smaller d3 d1)
(smaller d3 d2)

(on d1 source)
(on d2 d1)
(on d3 d2)

(clear d3)
(clear auxillary)
(clear destination)
)
(:goal
(and
(on d1 destination)
(on d2 d1)
(on d3 d2)
)
)
)
