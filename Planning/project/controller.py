from generator.generator import Generator
from solver.solver import Solver
from parser.ff_to_action import FFToActionParser
# generator
grid_desk='-x 5 -y 5 -t 15 -k 20 -l 20 -p 100'
pddl = 'grid'
g = Generator()
g.gen_problem_states(pddl, 100,grid_desk)
s = Solver()
s.solve_generated_states(pddl)

p = FFToActionParser()
p.parse_all(pddl)
