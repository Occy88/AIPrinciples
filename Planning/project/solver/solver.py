import os
import subprocess


class Solver:
    def __init__(self):
        pass

    def solve_generated_states(self, problem):
        os.chdir('./solver/FF-X')
        solution_dir = '../plans/' + problem
        domain = '../../domains/' + problem + '.pddl'
        state_dir = '../../generator/blocksworld/states/'
        os.popen('rm -rf ' + solution_dir + ' ; mkdir ' + solution_dir)

        for s in os.listdir(state_dir):
            print(s)
            os.popen(
                './ff -o ' + domain + ' -f ' + '../../generator/blocksworld/states/' + s + '| sed -n "/step/,/time/p" > ' + solution_dir + '/' + s)
        print(os.getcwd())
