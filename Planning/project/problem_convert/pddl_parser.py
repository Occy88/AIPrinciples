
from lark import Lark, Transformer, v_args

class PddlToJson(Transformer):
    def pddl(self, args):
        domain = args[0]
        predicates = args[1]
        actions = args[2:]
        return {'domain': domain, 'predicates': predicates, 'actions': actions}

    def string(self, s):
        return s[0].replace('-', '_')

    def predicates(self, p_list):
        return p_list

    def predicate(self, args):
        name = args[0]
        vals = list(tuple(args[1:]))
        p = {'name': name, 'args': vals}
        return p

    def var(self, v):
        val = v[0]
        return val

    def parameters(self, args):
        return list(args)

    def definition(self, name):
        return name

    def action(self, args):
        name, parameters, precondition, effect = args
        return {'name': name, 'args': parameters, 'precondition': precondition, 'effect': effect}

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

def parse_pddl(file):
    sample_conf = open(file, 'r').read()
    import os
    print(os.getcwd())
    grammar = open("problem_convert/grammar", 'r').read()
    print(sample_conf)
    print(grammar)
    parser = Lark(grammar, transformer=PddlToJson(), parser="lalr")
    return parser.parse(sample_conf)
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
# action(name,t) -> cl class UserObjectLevelPermission(permissions.BasePermission):
#     """
#        A Permission class to authenticate the user to an object
#        """
#
#     def has_permission(self, request, view):
#         path_items = view.kwargs.get('object_permission_id', None)
#         object_instance = locate(settings.USER_OBJECT_PERMISSION_INSTANCE).objects.get(pk=path_items)
#         if request.user.has_perm(settings.USER_OBJECT_PERMISSION, object_instance):
#             return True
#         else:
#             raise PermissionDenied({"message": "You are not authenticated to this the entity receiving the delivery",
#                                     "object_permission_id": object_instance.id})
#
# action(name,t) -> on(bm,bf)
#
#
#
pddl = {'domain': 'blocksworld',
        'predicates': [{'name': 'clear', 'args': list({'x'})},
                       {'name': 'on-table', 'args': list({'x'})},
                       {'name': 'on', 'args': list({'x', 'y'})}],
        'actions': [
            {'name': 'move-b-to-b',
             'args': list({'bf', 'bt', 'bm'}),
             'precondition': [{'name': 'clear', 'args': list({'bm'})},
                              {'name': 'clear', 'args': list({'bt'})},
                              {'name': 'on', 'args': list({'bf', 'bm'})}],
             'effect': {
                 'positive': [{'name': 'on', 'args': list({'bt', 'bm'})},
                              {'name': 'clear', 'args': list({'bf'})}],
                 'negative': [{'name': 'clear', 'args': list({'bt'})},
                              {'name': 'on', 'args': list({'bf', 'bm'})}]}},

            {'name': 'move-b-to-t', 'args': list({'bf', 'bm'}),
             'precondition': [{'name': 'clear', 'args': list({'bm'})},
                              {'name': 'on', 'args': list({'bf', 'bm'})}],
             'effect': {
                 'positive': [{'name': 'on-table', 'args': list({'bm'})},
                              {'name': 'clear', 'args': list({'bf'})}],
                 'negative': [{'name': 'on', 'args': list({'bf', 'bm'})}]}},
            {'name': 'move-t-to-b', 'args': list({'bt', 'bm'}),
             'precondition': [{'name': 'clear', 'args': list({'bm'})},
                              {'name': 'clear', 'args': list({'bt'})},
                              {'name': 'on-table', 'args': list({'bm'})}],
             'effect': {'positive': [{'name': 'on', 'args': list({'bt', 'bm'})}],
                        'negative': [{'name': 'clear', 'args': list({'bt'})},
                                     {'name': 'on-table', 'args': list({'bm'})}]}}]}


class freeze:
    def __init__(self):
        self.list = []
        self.unique = set()

    def __getitem__(self, item):
        return self.list[item]

    def __add__(self, other):
        if other in self.unique:
            return
        self.list.append(other)
        self.unique.add(other)

    def __hash__(self):
        return hash(str(self.list))
