import os
from os import listdir
from os.path import join


def get_plan(domain_path, p_path):
    return run_ff(domain_path, p_path)


def get_plans(domain_path, p_dir):
    plans = []
    for f in listdir(p_dir):
        print('getting_plan:', f)
        plans.append(get_plan(domain_path, join(p_dir, f)))
        # break
    return plans


def run_ff(domain, problem):
    cmd = 'ff -o ' + domain + ' -f ' + problem
    # cmd='pwd'
    # print('EXECUTING: ', cmd)
    stream = os.popen(cmd)
    return stream.read()


d = 'depotsstrips/Depots.pddl'
p = 'depotsstrips/pfiles'

pl = get_plans(d, p)
for p in pl:
    print(p)
