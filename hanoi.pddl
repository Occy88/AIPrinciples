;Header and description

(define (domain hanoi)

;remove requirements that are not needed
(:requirements :strips :fluents :typing :conditional-effects :negative-preconditions :equality :disjunctive-preconditions)

(:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
    disk
    base
)
; un-comment following line if constants are needed
;(:constants )
;todo: define predicates here
(:predicates 
    (clear ?x)
    (on ?x ?y)
    (smaller ?x ?y)
    (base ?x)
    (disk ?x )
)


(:functions ;todo: define numeric functions here
)

;define actions here
(:action mv
    :parameters (?obj ?from ?to)
    :precondition (and 
        (disk ?obj)
        (clear ?to)
        (clear ?obj)
        (on ?obj ?from)
        ;the destination is either a larger disk or the base.
        (or 
          (smaller ?obj ?to)
          (base ?to)
        )
    )
    :effect (and
        (clear ?from)
        (on ?obj ?to)
        (not (clear ?to))
        (not (on ?obj ?from))
    )
)

)