from pracmln import MLN
results=open("results",'w')
# state.perform_action('move-b-to-t', ('b9', 'b4'))
mln_params = 'mln_params_r.mln'
mln_database = 'mln_db_r.mln'
logic = 'FirstOrderLogic'
grammar = 'StandardGrammar'
method = 'pseudo-log-likelihood'
mln = MLN(logic, grammar, mln_params)
from pracmln import Database
import numpy as np
# print(np.exp(10),np.exp(100),np.exp(1000),np.exp(100000000000))
class pr():
    def write(self,*args,**kwargs):
        print(args,kwargs)
mln.write(pr())
mln.write(results)
db = Database.load(mln, mln_database)
result=mln.learn(db)

result.write(pr())

result.write(results)