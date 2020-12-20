from Planning.pddl_lib.pddlpy.pddlParser import pddlParser
def list2str(list_):
    return ", ".join([str(elem) for elem in list_])

def get_operator(ctx, operator_cls):
    from antlr4.tree.Tree import TerminalNodeImpl
    operator_name_list = []
    for child in ctx.getChildren():
        if child.getText() in ["(", ")"]:
            continue
        elif isinstance(child, (TerminalNodeImpl,
                                pddlParser.TimeSpecifierContext, pddlParser.IntervalContext, pddlParser.DurOpContext)):
            operator_name_list.append(child.getText())
        else:
            break
    if not operator_name_list:
        return None
    operator_name = " ".join(operator_name_list)
    return operator_cls(operator_name)

