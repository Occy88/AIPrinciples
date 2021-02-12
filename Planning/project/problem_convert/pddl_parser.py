import sys

from lark import Lark, Transformer, v_args

class Action:
    def __init__(self,action):
        self.pos=action['effect']['positive']
        self.neg=action['effect']['negative']
class State:
    def __init__(self,state):

        self.actions=state['actions']

    def _set_actions(self,actions):
        for a in actions:
            self.actions['']
class PddlToJson(Transformer):
    def pddl(self, args):
        domain = args[0]
        predicates = args[1]
        actions = args[2:]
        return {'domain': domain, 'predicates': predicates, 'actions': actions}

    def string(self, s):
        return s

    def predicates(self, p_list):
        return p_list

    def predicate(self, args):
        name = args[0][0].value
        vals = frozenset(tuple(args[1:]))
        p = {'name': name, 'args': vals}
        return p

    def var(self, v):
        val = v[0][0].value
        return val

    def parameters(self, args):
        return frozenset(tuple(args))

    def definition(self, name):
        return name[0][0].value

    def action(self, args):
        name, parameters, precondition, effect = args
        return {'name': name[0].value, 'params': parameters, 'pre': precondition, 'effect': effect}

    def effect(self, p_set):
        negative = list()
        positive = list()
        for p in p_set:
            try:
                if p.data == 'n_predicate':
                    negative += (p.children)
            except Exception as e:
                positive.append(p)
            print(p)
        return {'positive': positive, 'negative': negative}

    def precondition(self, args):
        return args

    number = v_args(inline=True)(float)

sample_conf = open('./blocksworld.pddl', 'r').read()
grammar = open("./grammar", 'r').read()
print(sample_conf)
print(grammar)
parser = Lark(grammar, transformer=PddlToJson(), parser="lalr")
parsed = parser.parse(sample_conf)

print(parser.parse(sample_conf))
f = open('out.txt', 'w')


def write_action(name, params, predicate):
    p1 = '\n0.000000    ' + name + '('
    p2 = ','.join(params) + ' ,t) => '
    return p1 + p2 + predicate['name'] + '(' + ', '.join(list(predicate['args'])) + ', t+1)'


f.write("// predicate declarations")

for a in parsed['actions']:
    f.write('\n' + a['name'] + '(' + ','.join(a['params']) + ',t)')

for p in parsed['predicates']:
    f.write('\n' + p['name'] + ' (' + ','.join(p['args']) + ',t)')
f.write("\n\n// formulas: ")

for a in parsed['actions']:
    # f.write("\n\n// positives: ")
    for p in a['effect']['positive']:
        f.write(write_action(a['name'], a['params'], p))
    # f.write("\n\n// negatives: ")
    for p in a['effect']['negative']:
        f.write(write_action(a['name'], a['params'], p))
# #
# # $name
# move-b-to-b
#
# # $args
# {bm,bf,bt}
#
# # Preconditions
# action(name,t) -> clear(bm,t)
# action(name,t) -> clear(bt,t)
# action(name,t) -> on(bm,bf,t)
#
# # Positive
# action(name,t) -> on(bm,bt,t+1)
# action(name,t) ->  clear(bf,t+1)
#
# # Negative
# action(name,t) -> clear(bt,t+1)
# action(name,t) -> on(bm,bf)
#
#
#
pddl = {'domain': 'blocksworld',
        'predicates': [{'name': 'clear', 'args': frozenset({'x'})},
                       {'name': 'on-table', 'args': frozenset({'x'})},
                       {'name': 'on', 'args': frozenset({'x', 'y'})}],
        'actions': [
            {'name': 'move-b-to-b',
             'params': frozenset({'bf', 'bt', 'bm'}),
             'pre': [{'name': 'clear', 'args': frozenset({'bm'})},
                     {'name': 'clear', 'args': frozenset({'bt'})},
                     {'name': 'on', 'args': frozenset({'bf', 'bm'})}],
             'effect': {
                 'positive': [{'name': 'on', 'args': frozenset({'bt', 'bm'})},
                              {'name': 'clear', 'args': frozenset({'bf'})}],
                 'negative': [{'name': 'clear', 'args': frozenset({'bt'})},
                              {'name': 'on', 'args': frozenset({'bf', 'bm'})}]}},

            {'name': 'move-b-to-t', 'params': frozenset({'bf', 'bm'}),
             'pre': [{'name': 'clear', 'args': frozenset({'bm'})}, {'name': 'on', 'args': frozenset({'bf', 'bm'})}],
             'effect': {
                 'positive': [{'name': 'on-table', 'args': frozenset({'bm'})},
                              {'name': 'clear', 'args': frozenset({'bf'})}],
                 'negative': [{'name': 'on', 'args': frozenset({'bf', 'bm'})}]}},
            {'name': 'move-t-to-b', 'params': frozenset({'bt', 'bm'}),
             'pre': [{'name': 'clear', 'args': frozenset({'bm'})}, {'name': 'clear', 'args': frozenset({'bt'})},
                     {'name': 'on-table', 'args': frozenset({'bm'})}],
             'effect': {'positive': [{'name': 'on', 'args': frozenset({'bt', 'bm'})}],
                        'negative': [{'name': 'clear', 'args': frozenset({'bt'})},
                                     {'name': 'on-table', 'args': frozenset({'bm'})}]}}]}
