from pracmln import MLN
# state.perform_action('move-b-to-t', ('b9', 'b4'))
mln_params = 'mln_params.mln'
mln_database = 'mln_db.mln'
logic = 'FirstOrderLogic'
grammar = 'StandardGrammar'
method = 'pseudo-log-likelihood'
mln = MLN(logic, grammar, mln_params)
from pracmln import Database
db = Database.load(mln, mln_database)
mln.learn(db)
