from os import listdir
from os.path import join

from Planning.pddl_lib.pddlpy.domain_problem import DomainProblem
from Planning.pddl_parser.planner import Planner

# print(p)
print('=========ops=======')
pfile_dir = 'depotsstrips/pfiles'
domain_path = 'depotsstrips/Depots.pddl'

planner = Planner()


def get_plan(domain_path, p_path):
    return DomainProblem(domain_path, p_path)


def get_plans(domain_path, p_dir):
    plans = []
    for f in listdir(p_dir):
        plans.append(get_plan(domain_path, join(p_dir, f)))
        break
    return plans


plans = get_plans('depotsstrips/Depots.pddl', 'depotsstrips/pfiles')
p = plans[0]

action_keys = p.operators()
state = p.initialstate()


class InvalidType(Exception):
    pass


def perform_action(action_key, action_variables, state):
    """
        o.variable_list
        {'?x': 'Truck', '?y': 'Place', '?z': 'Place'}
        o.precondition_neg
        set()
        o.precondition_pos
        {('at', '?x', '?y')}
        o.effect_neg
        {('at', '?x', '?y')}
        o.effect_pos
        {('at', '?x', '?z')}
    """
    action = p.domain.operators[action_key]
    type_dict = action.variable_list
    for index, key in enumerate(type_dict.keys()):
        if not type_dict[key] == p.worldobjects()[action_variables[index]]:
            raise InvalidType(action_variables, type_dict)
    return state


perform_action("Drive", ('truck2', 'depot0', 'depot1'), state)

print('=========world obj=======')
print(list(p.worldobjects()))
p._typesymbols()
print(p)
