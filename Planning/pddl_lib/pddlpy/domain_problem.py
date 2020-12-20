import itertools

from Planning.pddl_lib.pddlpy.domain_listener import DomainListener
from Planning.pddl_lib.pddlpy.operators import Operator
from Planning.pddl_lib.pddlpy.pddlLexer import CommonTokenStream
from Planning.pddl_lib.pddlpy.pddlLexer import FileStream
from Planning.pddl_lib.pddlpy.pddlLexer import pddlLexer
from Planning.pddl_lib.pddlpy.pddlParser import ParseTreeWalker
from Planning.pddl_lib.pddlpy.pddlParser import pddlParser
from Planning.pddl_lib.pddlpy.problem_listener import ProblemListener


class DomainProblem():

    def __init__(self, domainfile, problemfile):
        """Parses a PDDL domain and problem files and
        returns an object representing them.

        domainfile -- path for the PDDL domain file
        problemfile -- path for the PDDL problem file
        """
        # domain
        inp = FileStream(domainfile)
        lexer = pddlLexer(inp)
        stream = CommonTokenStream(lexer)
        parser = pddlParser(stream)
        tree = parser.domain()
        self.domain = DomainListener()
        walker = ParseTreeWalker()
        walker.walk(self.domain, tree)
        # problem
        inp = FileStream(problemfile)
        lexer = pddlLexer(inp)
        stream = CommonTokenStream(lexer)
        parser = pddlParser(stream)
        tree = parser.problem()
        self.problem = ProblemListener()
        walker = ParseTreeWalker()
        walker.walk(self.problem, tree)
        # variable ground space
        self.vargroundspace = []

    def operators(self):
        """Returns an iterator of the names of the actions defined in
        the domain file.
        """
        return self.domain.operators.keys()

    def ground_operator(self, op_name):
        """Returns an interator of Operator instances. Each item of the iterator
        is a grounded instance.

        returns -- An iterator of Operator instances.
        """
        op = self.domain.operators[op_name]
        for ground in self._instantiate( op.variable_list.items() ):
            st = dict(ground)
            gop = Operator(op_name)
            gop.variable_list = st
            gop.precondition_pos = set( [ a.ground( st ) for a in op.precondition_pos ] )
            gop.precondition_neg = set( [ a.ground( st ) for a in op.precondition_neg ] )
            gop.effect_pos = set( [ a.ground( st ) for a in op.effect_pos ] )
            gop.effect_neg = set( [ a.ground( st ) for a in op.effect_neg ] )
            yield gop

    def _typesymbols(self, t):
        return ( k for k,v in self.worldobjects().items() if v == t )

    def _instantiate(self, variables):
        if not self.vargroundspace:
            for vname, t in variables:
                c = []
                for symb in self._typesymbols(t):
                    c.append((vname, symb) )
                self.vargroundspace.append(c)
        return itertools.product(*self.vargroundspace)

    def initialstate(self):
        """Returns a set of atoms (tuples of strings) corresponding to the intial
        state defined in the problem file.
        """
        return self.problem.initialstate

    def goals(self):
        """Returns a set of atoms (tuples of strings) corresponding to the goals
        defined in the problem file.
        """
        return self.problem.goals

    def worldobjects(self):
        """Returns a dictionary of key value pairs where the key is the name of
        an object and the value is it's type (None in case is untyped.)
        """
        return dict( self.domain.objects.items() | self.problem.objects.items() )

