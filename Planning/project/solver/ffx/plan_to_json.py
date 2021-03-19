import sys

from lark import Lark, Transformer, v_args


class PddlToJson(Transformer):
    def plan(self, args):
        predicates = args[:-1]
        time = args[len(args) - 1]
        return {'steps': predicates, 'time': time}

    def string(self, s):
        # d=s.value
        # d2=s.lower()
        d3=s[0]
        d4=d3.value.lower().replace('-','_')
        return d4

    def predicate(self, args):
        name = args[0][0]
        vals = list(args[1:])
        p = {'name': name, 'args': vals}
        return p

    def arg(self, v):
        val = v[0]
        return val

    def action_name(self, s):
        return s

    def step(self, args):
        return {'step': args[0], 'predicate': args[1]}

    number = v_args(inline=True)(float)


import os


def parse_plan(domain_name, state_id):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '../plans/', '/'.join((domain_name, state_id)))
    sample_conf = open(filename, 'r').read()
    grammar = open(os.path.join(dirname, 'grammar'), 'r').read()
    parser = Lark(grammar, transformer=PddlToJson(), parser="lalr")
    parsed = parser.parse(sample_conf)
    return parsed


#
# def write_action(name, predicate):
#     p1 = '\n0.000000    action('
#     p2 = ' ,t) => '
#     return p1 + name + p2 + predicate['name'] + '(' + ', '.join(list(predicate['args'])) + ', t+1)'
#
#
# for p in parsed['predicates']:
#     f.write("// predicate declarations")
#     f.write('\n' + p['name'] + ' (' + ','.join(p['args']) + ')')
# f.write("\n\n// formulas: ")
#
# for a in parsed['actions']:
#     # f.write("\n\n// positives: ")
#     for p in a['effect']['positive']:
#         f.write(write_action(parsed['domain'], p))
#     # f.write("\n\n// negatives: ")
#     for p in a['effect']['negative']:
#         f.write(write_action(parsed['domain'], p))
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
plan = {'steps': [{'step': 0.0, 'predicate': {'name': 'MOVE-B-TO-T', 'args': list({'B7', 'B4'})}},
                  {'step': 1.0, 'predicate': {'name': 'MOVE-B-TO-B', 'args': list({'B5', 'B7', 'B4'})}},
                  {'step': 2.0, 'predicate': {'name': 'MOVE-B-TO-B', 'args': list({'B9', 'B1', 'B4'})}},
                  {'step': 3.0, 'predicate': {'name': 'MOVE-B-TO-T', 'args': list({'B1', 'B2'})}},
                  {'step': 4.0, 'predicate': {'name': 'MOVE-B-TO-T', 'args': list({'B3', 'B2'})}},
                  {'step': 5.0, 'predicate': {'name': 'MOVE-B-TO-B', 'args': list({'B3', 'B10', 'B1'})}},
                  {'step': 6.0, 'predicate': {'name': 'MOVE-T-TO-B', 'args': list({'B3', 'B8'})}},
                  {'step': 7.0, 'predicate': {'name': 'MOVE-B-TO-B', 'args': list({'B9', 'B8', 'B4'})}},
                  {'step': 8.0, 'predicate': {'name': 'MOVE-B-TO-B', 'args': list({'B5', 'B10', 'B6'})}},
                  {'step': 9.0, 'predicate': {'name': 'MOVE-T-TO-B', 'args': list({'B6', 'B2'})}}],
        'time': ('time', [0.0, 1200.0, 0.0])}
