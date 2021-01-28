import sys

from lark import Lark, Transformer, v_args


# class PddlToJson(Transformer):
#     @v_args(inline=True)
#     def string(self, s):
#         return s[1:-1].replace('\\"', '"')
#
#     array = list
#     pair = tuple
#     object = dict
#     number = v_args(inline=True)(float)
#
#     null = lambda self, _: None
#     true = lambda self, _: True
#     false = lambda self, _: False


sample_conf = open('./blocksworld.pddl', 'r').read()
grammar = open("./grammar", 'r').read()
print(sample_conf)
print(grammar)
parser = Lark(grammar, parser="lalr")

print(parser.parse(sample_conf).pretty())

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
