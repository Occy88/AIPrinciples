(define (domain gridworld)
    (:requirements :adl  :conditional-effects )
    (
    (:predicates
        (num ?x)
        (cell ?c)
        (black ?c )
        (value ?c  ?n )
        (conn ?c1 ?c2 )
        (lit ?c)
        (inc ?n1 ?n2))

    (:action place-bulb
        :parameters (?c)
        :precondition (and
                        (not (lit ?c))
                        (not(black ?c))
                        ; make sure that any connected black cells with value can be incremented (illegal otherwise)
                     )
        :effect ( and
            ; light up cell
            (lit ?c)
            ; increment all adjacent black cells with a value.
            (forall (?c1 ?n1  ?n2 )
                (when
                  (and
                  (inc ?n1 ?n2)
                  (conn ?c ?c1)
                  (black ?c1)
                  (value ?c1 ?n1))
                  (and
                  (not (value ?c1 ?n1))
                  (value ?c1 ?n2))))

        )
    )
    (:derived (lit ?x)
        (or

)