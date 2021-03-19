from lark import Lark, Transformer, v_args


class PddlToJson(Transformer):
    def problem(self, args):
        definition = args[0]
        domain = args[1]
        objects = args[2]
        init = args[3]
        goal = args[4]
        return {'definition': definition, 'domain': domain, 'objects': objects, 'init': init[0],
                'goal': goal[0]}

    def var(self, v):
        val = v[0][0].value
        return val

    def parameters(self, args):
        return list(args)

    def definition(self, name):
        return name

    def domain(self, name):
        return name

    def predicate(self, args):
        name = args[0]
        vals = list(tuple(args[1:]))
        p = {'name': name, 'args': vals}
        return p

    init = list

    predicates = list
    objects = list
    goal = list

    def string(self, s):
        s=s[0].value
        return s.replace('-','_')

    number = v_args(inline=True)(float)

import os

def parse_state(domain_name, state_id):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '/'.join((domain_name,'states',state_id)))
    sample_domain = open( filename, 'r').read()
    grammar = open(os.path.join(dirname,'grammar'), 'r').read()
    parser = Lark(grammar, transformer=PddlToJson(), parser="lalr")
    parsed = parser.parse(sample_domain)
    return parsed
