(define (domain gripper)
(:predicates (gripper ?gripper)
             (location ?location)
             (arm ?arm)
             (ball ?ball)
             (at_g ?gripper ?location)
             (at ?ball ?location)
             (belongs_to ?arm ?gripper)
             (empty ?arm)
             )

(:action pickup
  :parameters (?loc ?grip ?arm ?ball )
  :precondition (and (empty ?arm) (at_g ?grip ?loc) (at ?ball  ?loc) (belongs_to ?arm ?grip))
  :effect (and (at ?ball ?arm)
               (not (empty ?arm))
               (not (at ?ball  ?loc))
               ))

(:action move
  :parameters (?grip ?from ?to)
  :precondition (and (at_g ?grip ?from))
  :effect (and (not (at_g ?grip ?from))
               (at_g ?grip ?to)
               ))

(:action drop
  :parameters (?loc ?grip ?arm ?ball )
  :precondition (and (not(empty ?arm)) (at_g ?grip ?loc) (at ?ball  ?arm) (belongs_to ?arm ?grip))
  :effect (and (at ?ball  ?loc)
               (empty ?arm)
               (not (at ?ball  ?arm))
               ))
)

