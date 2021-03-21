import copy


class Predicate:
    def __init__(self, name='', args='9', arg_types='number'):
        self.name = name
        self.args = args
        self.arg_set = set(args)
        self.arg_types = arg_types
        self.weight = 0.0

    def _get_mln_str(self, args_to_use, cap_args, extra_args):
        args = copy.copy(args_to_use)
        if cap_args:
            args = list(map(lambda x: x.capitalize(), self.args))
        args += extra_args
        return self.name + '(' + ', '.join(args) + ')'

    def mln(self, cap_args=False, extra_args=[]):
        return self._get_mln_str(self.args, cap_args, extra_args)

    def mln_type(self, cap_args=False, extra_args=[]):
        return self._get_mln_str(self.arg_types, cap_args, extra_args)

    def __copy__(self):
        return Predicate(self.name, self.args)

    def __hash__(self):
        return hash(self.name + str(self.args))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        return " ".join((self.name, ": ", " ".join(self.args)))

    def get_property_hash(self, properties):
        """
        Concatenates multiple properties of object
        returns hash of resulting string
        Args:
            properties:
        Returns:

        """
        p_vals = ''
        for p in properties:
            p_vals += str(getattr(self, p))
        return hash(p_vals)

    @staticmethod
    def from_str(p_str):
        sp = p_str.split("(")
        args = sp[1]
        args = args.strip(")").replace(' ', '').split(',')
        return Predicate(sp[0], args)

    @staticmethod
    def exists_in_list_by_properties(predicate, predicate_list, properties):
        """
        Tests if there is a predicate with the same name in a list of predicates
        Args:
            predicate:
            predicate_list:

        Returns: Boolean

        """
        for p in predicate_list:
            if p.get_property_hash(properties) == predicate.get_property_hash(properties):
                return True
        return False

    @staticmethod
    def match_arguments(p_parent, p_child):
        """
        returns list of of indices of childs arguments present in the parent
        -1 if no match is found.
        e.g.
        p_parent.args=[a,b,c,d]
        p_child.args=[c,a,z]
        => [2,0,-1]
        Args:
            p_parent:
            p_child:

        Returns:
        """
        matching_list = []
        for p in p_child.args:
            try:
                matching_list.append(p_parent.args.index(p))
            except ValueError:
                matching_list.append(-1)
        return matching_list

    @staticmethod
    def matching_as_variables(p_parent, p_child):
        """
        uses match_arguments, converts to variable names (V1 V2)
        for any -1's for now we simply set them as the value of the argument
        assume it is not a variable for now.
        Args:
            p_parent:
            p_child:

        Returns:
        """
        matching_i = Predicate.match_arguments(p_parent, p_child)
        matching_v = []
        for i, v in enumerate(matching_i):
            if int(v) < 0:
                matching_v.append(p_child.args[i])
            else:
                matching_v.append('V' + str(v))
        return matching_v

    @staticmethod
    def unique_by_name(predicate_list):
        """
        returns unique set of predicates from list by name.
        Args:
            predicate_list:

        Returns:
        """
        unique_names = set()
        unique_preds = set()
        for p in predicate_list:
            if p.name not in unique_names:
                unique_preds.add(p)
                unique_names.add(p.name)
        return unique_preds


class Action:
    arg_locations = dict()

    def __init__(self, name='', args='', precondition='', effect=dict):
        self.name = name
        self.args = args
        self._set_arg_locations()
        self.precondition = precondition
        self.pos = self._get_predicates(effect['positive'])
        self.neg = self._get_predicates(effect['negative'])

    def _set_arg_locations(self):
        self.arg_locations = dict()
        for i, a in enumerate(self.args):
            self.arg_locations[a] = i

    def get_pos_list(self, args):
        return self.get_list(self.pos, args)

    def get_neg_list(self, args):
        return self.get_list(self.neg, args)

    def get_list(self, eff_list, args):
        """
        applies predicate on the positive/neg effects of an action
        and returns the list of predicates that are generated by said action.
        """
        if len(args) < len(self.args):
            raise Exception(
                "Arguments do not match Action footprint,\n expecting: " + str(self.args) + " | got: " + str(args))
        l = set()

        for p in eff_list:
            pc = p.__copy__()
            pc.args = list(map(lambda x: args[x], list(map(lambda y: self.arg_locations[y], p.args))))
            l.add(pc)
            # print(l)
        return l

    def _get_predicates(self, effect):
        l = []
        for p in effect:
            l.append(Predicate(**p))
        return l

    def __hash__(self):
        return hash(str(self.name) + str(self.args))


class State:
    actions = dict()

    def __init__(self, state):
        self._set_actions(state['actions'])
        self.state = set()
        self.latest_removed = set()
        self.latest_added = set()
        # self.latest_added=set()

    def perform_action(self, p: Predicate):
        # print(self)
        pos = self.actions[p.name].get_pos_list(p.args)
        self.state = self.state | pos
        self.latest_added = pos
        neg = self.actions[p.name].get_neg_list(p.args)
        self.latest_removed = neg
        self.state = self.state - neg

    def _set_actions(self, actions):
        for a in actions:
            self.actions[a['name']] = Action(**a)

    def set_init_state(self, predicate_json):
        for p in predicate_json:
            s = Predicate(**p)
            self.state.add(Predicate(**p))

    def mln(self, cap_args=False, extra_args=[]):
        s = ''
        for p in self.state:
            s += '\n' + p.mln(cap_args=cap_args, extra_args=extra_args)
        return s

    def __str__(self):
        for p in self.state:
            return str(p)


from pracmln import MLN
from itertools import chain


class Database:
    def __init__(self, action: Predicate, state: set, pos_effects: set, neg_effects: set):
        self.action = action
        self.state = state
        self.pos_effects = pos_effects
        self.neg_effects = neg_effects
        # precompute s why not...
        self.relevant_state_predicates = self.get_relevant_state_predicates()

    def get_relevant_state_predicates(self):
        """
        returns all predicates that have an argument that is present in
        the action's argument.
        Returns:
        """
        s = set()
        for p in chain(self.state, self.pos_effects, self.neg_effects):
            # TODO exclusion should not be limited to on? thi is to be discussed
            s.add(p)
            # if len(self.action.arg_set.intersection(p.arg_set)) > 0 and len(
            #         p.arg_set.difference(self.action.arg_set)) < 2:
            #     s.add(p)

        return s

    def mln_db(self):
        a = self.action.mln()
        p = ''
        for pr in chain(self.state, self.neg_effects, self.pos_effects):
            p += pr.mln() + '\n'
        return a + '\n' + p

    @staticmethod
    def parse_db(db: str):
        p_str = db.split('\n')
        p_p = []
        for p in p_str:
            # remove comments
            p = p.split('//')[0]
            # avoid empty lines, not nice for now but whatever.
            if len(p) < 2:
                continue
            p_p.append(Predicate.from_str(p))
        pos_effects = set()
        neg_effects = set()
        state = set()
        action = ''
        for p in p_p:
            if p.args[-1] == '0':
                state.add(p)
            elif p.args[-1] == '1':
                pos_effects.add(p)
            elif p.args[-1] == '-1':
                neg_effects.add(p)
            else:
                if not action == '':
                    raise Exception("Multiple actions in database: ", p.name, action.name)
                action = p
        return Database(p_p[0], state, pos_effects, neg_effects)


from pracmln.mln.database import Database as DB


class StateInfrence:
    def __init__(self, predicate_file):
        self.predicate_file = predicate_file
        # set of markov logic networks
        self.action_mln = dict()
        self.action_weights = dict()
        self.action_rejected_weights = dict()
        self.action_pending_weights = dict()
        self.actions = dict()
        self.logic = 'FirstOrderLogic'
        self.grammar = 'StandardGrammar'
        self.method = 'pseudo-log-likelihood'
        pass

    def process_database(self, db: Database):
        self._new_action_process(db)

    def update_mln(self):
        print("UPDATING MLN")
        action = self.db.action
        # if action.name not in self.action_mln:

        predicates = open(self.predicate_file).read() + "\n\n// formulas: \n"
        weights = self.gen_weights(action)
        open('tmp.mln', 'w').write(predicates + weights)
        try:
            m = MLN(self.logic, self.grammar, mlnfile='tmp.mln')
        except Exception as e:
            print(e)
            return
        for i, w in enumerate(m.weights):
            m.weights[i] = float(w)
        # m.weights[1]=1
        # m.weights[2]=10
        # else:
        #     m = self.action_mln[action.name]
        open('tmp_db.mln', 'w').write(self.db.mln_db())
        db = DB.load(m, 'tmp_db.mln')

        res = m.learn(db)
        for i, w in enumerate(res.weights):
            self.action_weights[self.db.action.name][i].weight += w
            res.weights[i] += self.action_weights[self.db.action.name][i].weight
        print(res.weights)
        # res.weights[3] = 2
        self.action_mln[action.name] = res
        return res

    # def gen_predicates(self,action:Predicate):
    #     preds = Predicate.unique_by_name(self.action_weights[action.name])
    #     p_str=''
    #     for p in preds:
    #         p_str+=p.mln_type()
    def prune_weights(self, threshold):
        """
        Prunes weights, (adds them to rejected weights), this is to speed up
        training if some weights go below a given threshold.
        Args:
            threshold:
        Returns: None
        """
        for action_name, weights in self.action_weights.items():
            accepted = []
            # accepted_w=[]
            for p in weights:
                if p.weight < threshold:
                    self.action_rejected_weights[action_name].append(p)
                else:
                    accepted.append(p)
                    # accepted_w.append(p.weight)
            self.action_weights[action_name] = accepted

    def insert_weights(self):
        db = self.db
        relevant_weights = db.relevant_state_predicates
        # existing_weights=self.action_weights[db.action]
        # existing_rejected_weidghts=self.action_rejected_weights[db.action]
        db.action.arg_types = Predicate.matching_as_variables(db.action, db.action)

        if db.action.name not in self.action_weights:
            self.action_weights[db.action.name] = []
            self.action_pending_weights[db.action.name] = []
            self.action_rejected_weights[db.action.name] = []
            self.actions[db.action.name] = db.action
        for w in relevant_weights:
            w.arg_types = Predicate.matching_as_variables(db.action, w)
            if w in self.action_rejected_weights[db.action.name] or \
                    Predicate.exists_in_list_by_properties(w,
                                                           self.action_weights[db.action.name],
                                                           ['name', 'arg_types']):
                continue
            self.action_weights[db.action.name].append(w)

    def gen_weights(self, action: Predicate):
        s = ""
        for w in self.action_weights[action.name]:
            s += str(w.weight) + "    " + action.mln_type() + " => " + w.mln_type() + '\n'
        # print(s)
        return s

    def _new_action_process(self, db: Database):
        """
        Check if the action already exists, add it if it doesn't,
        find all relevant preconditions add them to the mln if there are new ones
        check for contradictions -> split into two mlns if there are

        Args:
            db:

        Returns:

        """
        self.db = db
        self.insert_weights()  # CREATES MLN'S
        self.update_mln()
