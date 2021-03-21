from generator.generator import Generator
from solver.solver import Solver
from parser.ff_to_action import FFToActionParser
# generator
grid_desk='-x 6 -y 6 -t 4 -k 2 -l 2 -p 100'
pddl = 'grid'
g = Generator()
g.gen_problem_states(pddl, 100,grid_desk)
s = Solver()
s.solve_generated_states(pddl)

p = FFToActionParser()
p.parse_all(pddl)
