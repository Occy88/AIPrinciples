from pracmln import MLN

results = open("results", 'w')
# state.perform_action('move-b-to-t', ('b9', 'b4'))
mln_params = 'mln_params_r.mln'
mln_database = 'mln_db.mln'
logic = 'FirstOrderLogic'
grammar = 'StandardGrammar'
method = 'pseudo-log-likelihood'
domain = 'grid'
from pracmln import Database
import numpy as np

#
# # print(np.exp(10),np.exp(100),np.exp(1000),np.exp(100000000000))
# class pr():
#     def write(self, *args, **kwargs):
#         print(args, kwargs)
#
#
from problem_convert.PlanTraceGen import StateInfrence
from problem_convert.PlanTraceGen import Database as DB
import os
import random

num_databases = 25
print("Loading database file: ")
databases = open(mln_database).read()
databases = databases.strip('\n').strip(' ').strip('---').split("---")
random.shuffle(databases)
databases = databases[:num_databases]
d_processed = []
print("Processing databases")
for i, d in enumerate(databases):
    print(i / len(databases))
    # cut out any blank databases.
    if len(d) < 20:
        pass

    d_processed.append(DB.parse_db(d))
print("initiating state inference")
s = StateInfrence(os.getcwd() + '/' + domain + '_p_decs.txt')
print("Initiating learning:")
opt_tracker = dict()
for i, d in enumerate(d_processed):
    if d.action.name=='unlock':
        continue
    if d.action.name not in opt_tracker:
        opt_tracker[d.action.name] = 0
    # systematic noise on move function
    if d.action.name == 'move' :
        if opt_tracker[d.action.name]>=1:
                # d.noise(0.3)
                d.sys_noise('conn(v0,v1,0)',0.5)

    else:
        continue
    #     pass

    print("=========[ processing db: ", d.action.name, i, '/', len(d_processed), ' ]===========')
    print(i / len(d_processed))
    s.process_database(d)

    # s.update_data_for_graph(i)
    # if opt_tracker[d.action.name] % 5 and not opt_tracker[d.action.name] == 0:
    #     s.prune_weights(d.action.name,2)
    opt_tracker[d.action.name] += 1
    s.save_data_for_graphing()
s = StateInfrence(os.getcwd() + '/' + domain + '_p_decs.txt')

StateInfrence.plot()
# m.prin
print("writing results")
# for k in iter(s.action_weights):
#     print("============[ ", k, " ]============")
#
#     for i, p in enumerate(s.action_weights[k]):
#         print(p.weight, "    ", s.actions[k].mln_type(), " => ", p.mln_type())
# print("done")
# result=mln.learn(db)
#
# result.write(pr())
#
# result.write(results)
