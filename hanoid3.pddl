(define (problem hanoi3) (:domain hanoi)
    
    ; p is a peg d is a disk (3 disks 3 poles.)
    (:objects b1 b2 b3 d1 d2 d3
    )

    (:init
        ;todo: put the initial state's facts and numeric values here
        ; types:
        (base b1) (base b2) (base b3)

        (disk d1) (disk d2) (disk d3)

        ; sizes
        (smaller d3 d2) (smaller d2 d1)

        ;positions
        (on d1 b1) (on d2 d1) (on d3 d2)

        ; what is clear
        (clear d3)
        (clear b2)
        (clear b3)
    )

    (:goal (and
        ;todo: put the goal condition here
        ;positions
        (on d1 b3) (on d2 d1) (on d3 d2)
    ))

    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)
