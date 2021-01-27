(define (domain blocksworld)
(:predicates (clear ?x)
             (on-table ?x)
             (on ?x ?y))

(:action move-b-to-b
  :parameters (?bm ?bf ?bt)
  :precondition (and (clear ?bm) (clear ?bt) (on ?bm ?bf))
  :effect (and (not (clear ?bt)) (not (on ?bm ?bf))
               (on ?bm ?bt) (clear ?bf)))


# $name
move-b-to-b

# $args
{bm,bf,bt}

# Preconditions
action(name,t) -> clear(bm,t)
action(name,t) -> clear(bt,t)
action(name,t) -> on(bm,bf,t)

# Positive
action(name,t) -> on(bm,bt,t+1)
action(name,t) ->  clear(bf,t+1)

# Negative
action(name,t) -> clear(bt,t+1)
action(name,t) -> on(bm,bf)




(:action move-b-to-t
  :parameters (?bm ?bf)
  :precondition (and (clear ?bm) (on ?bm ?bf))
  :effect (and (not (on ?bm ?bf))
               (on-table ?bm) (clear ?bf)))

(:action move-t-to-b
  :parameters (?bm ?bt)
  :precondition (and (clear ?bm) (clear ?bt) (on-table ?bm))
  :effect (and (not (clear ?bt)) (not (on-table ?bm))
               (on ?bm ?bt))))

