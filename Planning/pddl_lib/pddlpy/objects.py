from Planning.pddl_lib.pddlpy.datatypes import Obj
from Planning.pddl_lib.pddlpy.enums import DurationOperator
from Planning.pddl_lib.pddlpy.enums import EffectOperator
from Planning.pddl_lib.pddlpy.enums import GoalOperator
from Planning.pddl_lib.pddlpy.pddlParser import pddlParser
from Planning.pddl_lib.pddlpy.utils import list2str

class Atom():
    def __init__(self, predicate):
        self.predicate = predicate

    def __repr__(self):
        return str(tuple(self.predicate))

    def ground(self, varvals):
        g = [ varvals[v] if v in varvals else v for v in self.predicate ]
        return tuple(g)



class Goal(object):
    atom = None
    operator = None
    sub_goals = None
    obj = None

    def __init__(self, operator=None, sub_goals=None, atom=None, obj=None):
        self.operator = operator
        if atom:
            assert isinstance(atom, Atom)
            self.atom = atom
        elif operator in [GoalOperator.AND, GoalOperator.OR]:
            assert hasattr(sub_goals, "__iter__") and all(isinstance(goal, Goal) for goal in sub_goals)
            self.sub_goals = tuple(sub_goals)
        elif operator == GoalOperator.NOT:
            assert isinstance(sub_goals, Goal)
            self.sub_goals = (sub_goals,)
        elif operator == GoalOperator.IMPLY:
            assert hasattr(sub_goals, "__len__") and len(sub_goals) == 2 and all(
                isinstance(goal, Goal) for goal in sub_goals)
            self.sub_goals = tuple(sub_goals)
        elif operator in [GoalOperator.EXISTS, GoalOperator.FORALL]:
            assert isinstance(obj, Obj) and isinstance(sub_goals, Goal)
            self.obj = obj
            self.sub_goals = {sub_goals}
        elif operator in [GoalOperator.AT_START, GoalOperator.AT_END, GoalOperator.OVER_ALL]:
            assert isinstance(sub_goals, Goal)
            self.sub_goals = {sub_goals}

    def recursive_atoms(self):
        if self.atom:
            yield self.atom
        for goal in self.sub_goals or []:
            for atom in goal.recursive_atoms():
                yield atom

    def __repr_(self):
        if self.atom:
            return str(self.atom)
        elif self.operator in [GoalOperator.EXISTS, GoalOperator.FORALL]:
            return "({op} ({var}) {goals})".format(op=self.operator, var=self.obj, goals=list2str(self.sub_goals))
        else:
            return "({op} {goals})".format(op=self.operator, goals=list2str(self.sub_goals))

    def __str__(self):
        return self.__repr_()

    def __eq__(self, other):
        return isinstance(other, Goal) and \
               self.operator == other.operator and self.sub_goals == other.sub_goals and self.obj == other.obj


class Effect(object):
    atom = None
    operator = None
    sub_effects = None
    obj = None
    goal = None

    def __init__(self, operator=None, sub_effects=None, atom=None, obj=None, goal=None):
        self.operator = operator
        if operator is None:
            assert isinstance(atom, Atom)
            self.atom = atom
        elif operator == EffectOperator.AND:
            assert all(isinstance(effect, Effect) for effect in sub_effects)
            self.sub_effects = tuple(sub_effects)
        elif operator == EffectOperator.NOT:
            assert isinstance(sub_effects, Effect)
            self.sub_effects = (sub_effects,)
        elif operator == EffectOperator.WHEN:
            assert isinstance(goal, Goal) and isinstance(sub_effects, Effect)
            self.goal = goal
            self.sub_effects = (sub_effects,)
        elif operator == EffectOperator.FORALL:
            assert isinstance(obj, Obj) and isinstance(sub_effects, Effect)
            self.obj = obj
            self.sub_effects = (sub_effects,)
        elif operator in [EffectOperator.AT_START, EffectOperator.AT_END]:
            assert isinstance(sub_effects, Effect)
            self.sub_effects = (sub_effects,)

    def recursive_atoms(self):
        if self.atom:
            yield self.atom
        for effect in self.sub_effects or []:
            for atom in effect.recursive_atoms():
                yield atom
        if self.goal:
            for atom in self.goal.recursive_atoms():
                yield atom

    def __repr_(self):
        if self.operator is None:
            return str(self.atom)
        elif self.operator == EffectOperator.FORALL:
            return "({op} ({var}) {effects})".format(op=self.operator, var=self.obj, effects=list2str(self.sub_effects))
        elif self.operator == EffectOperator.WHEN:
            return "({op} {goal} {effects})".format(op=self.operator, goal=self.goal,
                                                    effects=list2str(self.sub_effects))
        else:
            return "({op} {effects})".format(op=self.operator, effects=list2str(self.sub_effects))

    def __str__(self):
        return self.__repr_()

    def __eq__(self, other):
        return isinstance(other, Effect) and \
               self.atom == other.atom and self.operator == other.operator and \
               self.sub_effects == other.sub_effects and self.obj == other.obj and self.goal is other.goal


class Duration(object):
    operator = None
    sub_durations = None
    value = None

    def __init__(self, operator=None, sub_durations=None, value=None):
        self.operator = operator
        if operator == DurationOperator.AND:
            assert hasattr(sub_durations, "__iter__") and all(
                isinstance(duration, Duration) for duration in sub_durations)
            self.sub_durations = set(sub_durations)
        elif operator in [DurationOperator.SE, DurationOperator.GE, DurationOperator.EQ]:
            assert value is not None
            self.value = value
        elif operator in [DurationOperator.AT_START, DurationOperator.AT_END]:
            assert isinstance(sub_durations, Duration)
            self.sub_durations = {sub_durations}

    def __repr_(self):
        if self.operator is None:
            return "()"
        elif self.operator in [DurationOperator.SE, DurationOperator.GE, DurationOperator.EQ]:
            return "({op} {value})".format(op=self.operator, value=self.value)
        else:
            return "({op} {durations})".format(op=self.operator, durations=list2str(self.sub_durations))

    def __str__(self):
        return self.__repr_()
