import os
from parser.action import Action
import json
import time


# definition of an action
class FFToActionParser:
    """
    Parses oiutput (modified with sed command) from ff
    to a list of actions (plan traces that can be interpreted for
    ML.
    """

    def __init__(self):
        pass

    def _clean_text(self, text):
        """
        removes step and final line from:
        step    0: MOVE-B-TO-T B2 B1
        1: MOVE-B-TO-T B3 B10
        ....
        10: MOVE-T-TO-B B6 B3


        time spent:    0.00 seconds instantiating 1200 easy, 0 hard action templates

        """
        # for now ignore this, take care of parsing properly in parse_line...
        return text

    def _convert_to_action(self, text):
        """
        converts: MOVE-T-TO-B B9 B6
        to an action in the form:
        action_name & arguments
        """
        text = text.strip().split(' ')
        return (text[0], text[1:])

    def _parse_line(self, line):
        arr = line.split(':')
        if len(arr) <= 1:
            raise Exception

        if 'step' in arr[0] or int(arr[0]):
            return self._convert_to_action(arr[1])

    def _parse_text(self, text):
        """
        returns set of actions.
        """
        text = self._clean_text(text)
        trace = []
        for line in text.split('\n'):
            try:
                trace.append(self._parse_line(line))
            except Exception:
                continue
        return trace
        pass

    def parse_all(self, problem):
        """
        writes output to json saves each output into a new state file.
        """
        print("=================================")
        print(os.getcwd())
        os.chdir('./parser/plan_traces')

        os.popen('rm -rf ' + problem + ' ; mkdir ' + problem)
        print(os.getcwd())
        for name in os.listdir('../../solver/plans/' + problem):
            print(name)
            f = open('../../solver/plans/' + problem + '/' + name)
            text = f.read()
            f.close()
            parsed = self._parse_text(text)
            f = open('./' + problem + '/' + name, 'w+')
            print(parsed)
            f.write(json.dumps(parsed))
            f.close()

        print(os.getcwd())
