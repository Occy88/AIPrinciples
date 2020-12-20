from Planning.pddl_lib.pddlpy.datatypes import Scope


class Operator():
    """Represents and action. Can be grounded or ungrounded.
    Ungrounded operators have a '?' in names (unbound variables).
    Attributes:

        operator_name -- the name of operator (action in the domain.)
        variable_list -- a dictionary of key-value pairs where the key
                         is the variable name (with the '?') and the
                         value is the value of it when the operator is
                         grounded.
        precondition_pos -- a set of atoms corresponding to the
                            positive preconditions.
        precondition_neg -- a set of atoms corresponding to the
                            negative preconditions.
        effect_pos -- a set of atoms to add.
        effect_neg -- a set of atoms to delete.
    """
    def __init__(self, name):
        self.operator_name = name
        self.variable_list = {}
        self.precondition_pos = set()
        self.precondition_neg = set()
        self.effect_pos = set()
        self.effect_neg = set()




class Action(Operator):
    """Represents an action. Can be grounded or ungrounded.
    Ungrounded operators have a '?' in names (unbound variables).
    Attributes:

        precondition -- a possiby nested Goal
        condition -- a possiby nested Goal
    """

    def __init__(self, name):
        super(Action, self).__init__(name)
        self.precondition = None

    def effects_and_conditions(self):
        conditions = [self.precondition] if self.precondition else []
        return super(Action, self).effects_and_conditions() + conditions


class DurativeAction(Operator):
    """Represents an durative-action:

        duration -- a possibly nested Duration
        condition -- a possibly nested Goal
    """

    def __init__(self, name):
        super(DurativeAction, self).__init__(name)
        self.duration = None
        self.condition = None

    def effects_and_conditions(self):
        conditions = [self.condition] if self.condition else []
        return super(DurativeAction, self).effects_and_conditions() + conditions
