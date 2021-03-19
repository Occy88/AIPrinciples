;towers of hanoi domain
(define (domain hanoi)

    (:requirements :strips)

    (:predicates    (smaller ?x ?y)
                    (on ?x ?y)
                    (clear ?x)
    )

    (   :action move
        :parameters (?disc ?from ?to)
        :precondition (and  (smaller ?disc ?to)
                            (on ?disc ?from)
                            (clear ?disc)
                            (clear ?to))
        :effect  (and
                    (clear ?from)
                    (on ?disc ?to)
                    (not (on ?disc ?from))
                    (not (clear ?to))
                  )
    )
)