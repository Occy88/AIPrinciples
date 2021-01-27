from Planning.project.generator.generator import Generator
from Planning.project.solver.solver import Solver
from Planning.project.parser.ff_to_action import FFToActionParser

# generator
pddl = 'blocksworld'
g = Generator()
g.gen_problem_states(pddl, 100)
s = Solver()
s.solve_generated_states(pddl)

p = FFToActionParser()
p.parse_all(pddl)
