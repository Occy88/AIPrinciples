import os
import subprocess
import time


class Solver:
    def __init__(self):
        pass

    def solve_generated_states(self, problem):
        print(os.getcwd())
        print(os.listdir())
        os.chdir('./solver/ffx')
        solution_dir = '../plans/' + problem
        domain = '../../domains/' + problem + '.pddl'
        state_dir = '../../generator/' + problem + '/states/'
        os.popen('rm -rf ' + solution_dir + ' ; mkdir ' + solution_dir)
        i=0
        for s in os.listdir(state_dir):
            i+=1
            print(i)
            # print(solution_dir)
            # print(os.getcwd())
            command = './ff -o ' + domain + ' -f ' + '../../generator/' + problem + '/states/' + s + '| sed -n "/step/,/time/p" > ' + solution_dir + '/' + s
            # command = './ff -o ' + domain + ' -f ' + '../../generator/' + problem + '/states/' + s + ' > ' + solution_dir + '/' + s
            # print(command)
            os.popen(command).read()
        os.chdir("../../")
