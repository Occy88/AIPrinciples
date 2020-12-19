from os import listdir
from os.path import join

import pddlpy

# print(p)
print('=========ops=======')
pfile_dir = 'depotsstrips/pfiles'
domain_path = 'depotsstrips/Depots.pddl'


def get_problem(domain_path, p_path):
    return pddlpy.DomainProblem(domain_path, p_path)


def get_problems(domain_path, p_dir):
    problems = []
    for f in listdir(p_dir):
        problems.append(get_problem(domain_path, join(p_dir, f)))
        break
    return problems


problems = get_problems('depotsstrips/Depots.pddl', 'depotsstrips/pfiles')
p = problems[0]

#
for p in problems:
    for o in p.operators():
        print(o)
        print('=========ground op=======')
        go = list(p.ground_operator(o))
        print()
        if len(go)>0:
            go=go[0]
        else:
            continue
        print("_________________")
        print(go.precondition_pos)
        print(go.precondition_neg)
# print('=========goals=======')
# for g in p.goals():
#     print(g)
# print('=========state=======')
# print(p.initialstate())
# # for s in p.initialstate():
# #     print(s)
#
# print('=========world obj=======')
# print(list(p.worldobjects()))
