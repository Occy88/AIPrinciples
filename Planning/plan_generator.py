from os import listdir
from os.path import join

from Planning.pddl_parser.planner import Planner

# print(p)
print('=========ops=======')
pfile_dir = 'depotsstrips/pfiles'
domain_path = 'depotsstrips/Depots.pddl'

planner = Planner()


def get_plan(domain_path, p_path):
    return planner.solve(domain_path, p_path)


def get_plans(domain_path, p_dir):
    plans = []
    for f in listdir(p_dir):
        plans.append(get_plan(domain_path, join(p_dir, f)))
        break
    return plans


plans = get_plans('depotsstrips/Depots.pddl', 'depotsstrips/pfiles')
p = plans[0]
print(p)
