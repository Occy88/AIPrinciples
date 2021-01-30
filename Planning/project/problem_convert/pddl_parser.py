import sys

from lark import Lark, Transformer, v_args


class PddlToJson(Transformer):
    def pddl(self, args):
        domain = args[0]
        predicates = args[1]
        actions = args[2:]
        return {'domain': args[0], 'predicates': predicates, 'actions': actions}

    def string(self, s):
        return s

    def predicates(self, p_list):
        return p_list

    def predicate(self, args):
        name = args[0][0].value
        vals = frozenset(tuple(args[1:]))
        p = frozenset({name, vals})
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
        negative = set()
        positive = set()
        for p in p_set:
            try:
                if p.data == 'n_predicate':
                    negative.add(frozenset(p.children))
            except Exception as e:
                positive.add(p)
            print(p)
        return {'positive': positive, 'negative': negative}

    precondition = set
    number = v_args(inline=True)(float)


sample_conf = open('./blocksworld.pddl', 'r').read()
grammar = open("./grammar", 'r').read()
print(sample_conf)
print(grammar)
parser = Lark(grammar, transformer=PddlToJson(), parser="lalr")
parsed = parser.parse(sample_conf)

print(parser.parse(sample_conf))

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
