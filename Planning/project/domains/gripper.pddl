(define (domain gripper)
(:predicates (ball_at ?location)
             (gripper_at ?location)
             (belongs_to ?arm ?gripper)
             (empty ?arm)
             )

(:action pickup
  :parameters (?loc ?grip ?arm ?ball )
  :precondition (and (empty ?arm) (gripper_at ?loc) (ball_at ?loc) (belongs_to ?arm ?grip))
  :effect (and (ball_at ?arm)
               (not (empty ?arm))
               (not (ball_at ?loc))
               ))

(:action move
  :parameters (?grip ?from ?to)
  :precondition (and (gripper_at ?from))
  :effect (and (not (gripper_at ?from))
               (gripper_at ?to)
               ))

(:action drop
  :parameters (?loc ?grip ?arm ?ball )
  :precondition (and (not(empty ?arm)) (gripper_at ?loc) (ball_at ?arm) (belongs_to ?arm ?grip))
  :effect (and (ball_at ?loc)
               (empty ?arm)
               (not (ball_at ?arm))
               ))
)

