from enum import Enum

class EffectOperator(Enum):
    AND = "and"
    NOT = "not"
    WHEN = "when"
    FORALL = "forall"
    AT_START = "at start"
    AT_END = "at end"

class GoalOperator(Enum):
    AND = "and"
    OR = "or"
    NOT = "not"
    IMPLY = "imply"
    EXISTS = "exists"
    FORALL = "forall"
    AT_START = "at start"
    AT_END = "at end"
    OVER_ALL = "over all"

class DurationOperator(Enum):
    AND = "and"
    AT_START = "at start"
    AT_END = "at end"
    SE = "<= ?duration"
    GE = ">= ?duration"
    EQ = "= ?duration"

