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
        return name[0].value

    def domain(self, name):
        return name[0].value

    def predicate(self, args):
        args = list(map(lambda x: x.value, args))
        name = args[0]
        vals = list(tuple(args[1:]))
        p = {'name': name, 'args': vals}
        return p

    init = list

    predicates = list
    objects = list
    goal = list

    def string(self, s):
        return s[0]

    number = v_args(inline=True)(float)

