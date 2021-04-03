(define (domain gridworld)
    (:requirements :adl  :conditional-effects )
    (:types
        xc ; x coordinates
        yc ;y coords
        v ; values of black squares (0->4)
    )
    (:predicates
        (black ?x - xc ?y - yc )
        (value ?x - xc ?y - yc  ?n - v  )
        (conn ?x1 - xc ?y1 - yc ?x2 - xc ?y2 - yc )
        (lit ?x - xc ?y - yc)
        (gx ?x ?x1 - xc)
        (gy ?y ?y1 - yc)
        (inc ?n1 - v ?n2 - v))

    ; only one action placing bulb in coord xcyc
    (:action place-bulb
        :parameters (?x - xc ?y - yc)
        :precondition (and
                        ; can't place a bulb on lit square or black square
                        (not (lit ?x ?y ))
                        (not(black ?x ?y ))
                     )
        :effect ( and
            ; light up cell
            (lit ?x  ?y)
            ; increment all adjacent black cells that have an associated value.
            (forall (?x1 - xc ?y1 - yc ?n1 - v  ?n2 - v)
                (when
                  (and
                  ; can be incremented
                  (inc ?n1 ?n2)
                  ; is connected to current square
                  (conn ?x ?y ?x1 ?y1)
                  ; is black and has a value
                  (black ?x1 ?y1)
                  (value ?x1 ?y1 ?n1))
                  (and
                  ;negate old value add new value
                  (not (value ?x1 ?y1 ?n1))
                  (value ?x1 ?y1 ?n2))))

            ; take care of horizontal light rays
            (forall (?x1 - xc)
                (when
                    (and
                        ; must not be back to light up
                        (not (black ?x1 ?y))
                        ; conditions for in-between cells (must not be black)
                        ; in english : if there are any cells xc2y between xcy & xc1y that are black do not light up xc1y

                        (not
                            (or
                            ; cells on the right
                            (exists (?x2 - xc) (and (gx ?x2 ?x1) (gx ?x ?x2) (black ?x2 ?y)) )
                            ;cells on the left
                            (exists (?x2 - xc) (and (gx ?x1 ?x2) (gx ?x2 ?x) (black ?x2 ?y)) )
                            )
                        )
                    )
                    (and (lit ?x1 ?y))
                )
            )
            ; take care of vertical light rays (copy of horizontal hence no comments)
            (forall (?y1 - yc)
                (when
                    (and
                        (not (black ?x ?y1))
                        (not
                            (or
                            (exists (?y2 - yc) (and (gy ?y2 ?y1) (gy ?y ?y2) (black ?x ?y2)) )
                            (exists (?y2 - yc) (and (gy ?y1 ?y2) (gy ?y2 ?y) (black ?x ?y2)) )
                            )
                        )
                    )
                    (and (lit ?x ?y1))
                )

            )

        )
    )
)