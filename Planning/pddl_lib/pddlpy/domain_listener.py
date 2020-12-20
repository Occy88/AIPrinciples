from Planning.pddl_lib.pddlpy.objects import Atom
from Planning.pddl_lib.pddlpy.objects import Duration
from Planning.pddl_lib.pddlpy.objects import DurationOperator
from Planning.pddl_lib.pddlpy.objects import Effect
from Planning.pddl_lib.pddlpy.objects import EffectOperator
from Planning.pddl_lib.pddlpy.objects import Goal
from Planning.pddl_lib.pddlpy.objects import GoalOperator
from Planning.pddl_lib.pddlpy.objects import Obj
from Planning.pddl_lib.pddlpy.operators import Action
from Planning.pddl_lib.pddlpy.operators import DurativeAction
from Planning.pddl_lib.pddlpy.operators import Operator
from Planning.pddl_lib.pddlpy.operators import Scope
from Planning.pddl_lib.pddlpy.pddlListener import pddlListener
from Planning.pddl_lib.pddlpy.pddlParser import pddlParser
from Planning.pddl_lib.pddlpy.utils import get_operator


class DomainListener(pddlListener):
    def __init__(self):
        self.typesdef = False
        self.objects = {}
        self.operators = {}
        self.scopes = []
        self.negativescopes = []

    def enterActionDef(self, ctx):
        opname = ctx.actionSymbol().getText()
        opvars = {}
        self.scopes.append(Operator(opname))

    def exitActionDef(self, ctx):
        action = self.scopes.pop()
        self.operators[action.operator_name] = action

    def enterPredicatesDef(self, ctx):
        self.scopes.append(Operator(None))

    def exitPredicatesDef(self, ctx):
        dummyop = self.scopes.pop()

    def enterTypesDef(self, ctx):
        self.scopes.append(Obj())

    def exitTypesDef(self, ctx):
        self.typesdef = True
        self.scopes.pop()

    def enterTypedVariableList(self, ctx):
        # print("-> tvar")
        # TODO supersets
        for v in ctx.VARIABLE():
            vname = v.getText()
            self.scopes[-1].variable_list[v.getText()] = None
        for vs in ctx.singleTypeVarList():
            t = vs.r_type().getText()
            for v in vs.VARIABLE():
                vname = v.getText()
                self.scopes[-1].variable_list[vname] = t

    def enterAtomicTermFormula(self, ctx):
        # print("-> terf")
        neg = self.negativescopes[-1]
        pred = []
        for c in ctx.getChildren():
            n = c.getText()
            if n == '(' or n == ')':
                continue
            pred.append(n)
        scope = self.scopes[-1]
        if not neg:
            scope.addatom(Atom(pred))
        else:
            scope.addnegatom(Atom(pred))

    def enterPrecondition(self, ctx):
        self.scopes.append(Scope())

    def exitPrecondition(self, ctx):
        scope = self.scopes.pop()
        self.scopes[-1].precondition_pos = set( scope.atoms )
        self.scopes[-1].precondition_neg = set( scope.negatoms )

    def enterEffect(self, ctx):
        self.scopes.append(Scope())

    def exitEffect(self, ctx):
        scope = self.scopes.pop()
        self.scopes[-1].effect_pos = set( scope.atoms )
        self.scopes[-1].effect_neg = set( scope.negatoms )

    def enterGoalDesc(self, ctx):
        negscope = bool(self.negativescopes and self.negativescopes[-1])
        for c in ctx.getChildren():
            if c.getText() == 'not':
                negscope = True
                break
        self.negativescopes.append(negscope)

    def exitGoalDesc(self, ctx):
        self.negativescopes.pop()

    def enterPEffect(self, ctx):
        negscope = False
        for c in ctx.getChildren():
            if c.getText() == 'not':
                negscope = True
                break
        self.negativescopes.append(negscope)

    def exitPEffect(self, ctx):
        self.negativescopes.pop()

    def enterTypedNameList(self, ctx):
        # print("-> tnam")
        # TODO super sets of object types
        print(ctx)
        for v in ctx.name():
            vname = v.getText()
            self.scopes[-1].variable_list[v.getText()] = None
        for vs in ctx.singleTypeNameList():
            t = vs.r_type().getText()
            for v in vs.name():
                vname = v.getText()
                self.scopes[-1].variable_list[vname] = t

    def enterConstantsDef(self, ctx):
        self.scopes.append(Obj())

    def exitConstantsDef(self, ctx):
        scope = self.scopes.pop()
        self.objects = scope.variable_list

    def exitDomain(self, ctx):
        if not self.objects and not self.typesdef:
            vs = set()
            for opn, oper in self.operators.items():
                alls = oper.precondition_pos | oper.precondition_neg | oper.effect_pos | oper.effect_neg
                for a in alls:
                    for s in a.predicate:
                        if s[0] != '?':
                            vs.add( (s, None) )
            self.objects = dict( vs)
