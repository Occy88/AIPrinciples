from Planning.project.generator.generator import Generator
from Planning.project.solver.solver import Solver

# generator
pddl = 'blocksworld'
# g = Generator()
# g.gen_problem_states(pddl, 100)
s = Solver()
s.solve_generated_states(pddl)
