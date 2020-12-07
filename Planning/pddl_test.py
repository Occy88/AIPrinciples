import pddlpy

p = pddlpy.DomainProblem('hanoi_domain.pddl', 'hanoi_problem.pddl')
print(p)
print('=========ops=======')
for o in p.operators():
    print(o)
    print('=========ground op=======')
    for go in p.ground_operator(o):
        print(go.precondition_pos)
        print(go.precondition_neg)
print('=========goals=======')

for g in p.goals():
    print(g)
print('=========state=======')

for s in p.initialstate():
    print(s)

print('=========world obj=======')
for o in p.worldobjects():
    print(o)
