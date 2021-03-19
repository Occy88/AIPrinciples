*** processed args: Namespace(alias=None, build='release32', components=['translate', 'preprocess', 'search'], filenames=['../../domains/gripper.pddl', '../../generator/gripper/states/state_1'], plan_file='sas_plan', planner_args=['../../domains/gripper.pddl', '../../generator/gripper/states/state_1', '--search', 'wastar(blind(),w=1)'], preprocess=False, preprocess_input='output.sas', preprocess_options=[], run_all=False, run_search=False, search_input='output', search_options=['--search', 'wastar(blind(),w=1)'], show_aliases=False, translate=False, translate_inputs=['../../domains/gripper.pddl', '../../generator/gripper/states/state_1'], translate_options=[])
INFO     Running translator.
INFO     callstring: /usr/bin/python /home/c4r4mel/PycharmProjects/AIPrinciples/Planning/project/solver/fd-stripped/builds/release32/bin/translate/translate.py ../../domains/gripper.pddl ../../generator/gripper/states/state_1
Parsing...
Parsing: [0.000s CPU, 0.001s wall-clock]
Normalizing task... [0.000s CPU, 0.000s wall-clock]
Instantiating...
Generating Datalog program... [0.000s CPU, 0.000s wall-clock]
Normalizing Datalog program...
Normalizing Datalog program: [0.000s CPU, 0.001s wall-clock]
Preparing model... [0.000s CPU, 0.000s wall-clock]
Generated 22 rules.
Computing model... [0.000s CPU, 0.002s wall-clock]
221 relevant atoms
160 auxiliary atoms
381 final queue length
561 total queue pushes
Completing instantiation... [0.000s CPU, 0.003s wall-clock]
Instantiating: [0.010s CPU, 0.007s wall-clock]
Computing fact groups...
Finding invariants...
8 initial candidates
Finding invariants: [0.000s CPU, 0.001s wall-clock]
Checking invariant weight... [0.000s CPU, 0.000s wall-clock]
Instantiating groups... [0.000s CPU, 0.000s wall-clock]
Collecting mutex groups... [0.000s CPU, 0.000s wall-clock]
Choosing groups...
2 uncovered facts
Choosing groups: [0.000s CPU, 0.000s wall-clock]
Building translation key... [0.000s CPU, 0.000s wall-clock]
Computing fact groups: [0.000s CPU, 0.002s wall-clock]
Building STRIPS to SAS dictionary... [0.000s CPU, 0.000s wall-clock]
Building dictionary for full mutex groups... [0.000s CPU, 0.000s wall-clock]
Building mutex information...
Building mutex information: [0.000s CPU, 0.000s wall-clock]
Translating task...
Processing axioms...
Simplifying axioms... [0.000s CPU, 0.000s wall-clock]
Processing axioms: [0.000s CPU, 0.000s wall-clock]
Translating task: [0.010s CPU, 0.004s wall-clock]
48 effect conditions simplified
0 implied preconditions added
Detecting unreachable propositions...
0 operators removed
4 propositions removed
Detecting unreachable propositions: [0.000s CPU, 0.001s wall-clock]
Translator variables: 6
Translator derived variables: 0
Translator facts: 36
Translator goal facts: 4
Translator mutex groups: 4
Translator total mutex groups size: 32
Translator operators: 152
Translator axioms: 0
Translator task size: 810
Translator peak memory: 19176 KB
Writing output... [0.000s CPU, 0.001s wall-clock]
Done! [0.020s CPU, 0.016s wall-clock]
INFO     Running preprocessor (release32).
INFO     callstring: /home/c4r4mel/PycharmProjects/AIPrinciples/Planning/project/solver/fd-stripped/builds/release32/bin/preprocess < output.sas
Building causal graph...
The causal graph is not acyclic.
6 variables of 6 necessary
0 of 4 mutex groups necessary.
152 of 152 operators necessary.
0 of 0 axiom rules necessary.
Building domain transition graphs...
solveable in poly time 0
Building successor generator...
Preprocessor facts: 36
Preprocessor derived variables: 0
Preprocessor task size: 778
Writing output...
done

INFO     Running search (release32).
INFO     search executable: /home/c4r4mel/PycharmProjects/AIPrinciples/Planning/project/solver/fd-stripped/builds/release32/bin/downward
INFO     callstring: /home/c4r4mel/PycharmProjects/AIPrinciples/Planning/project/solver/fd-stripped/builds/release32/bin/downward --search 'wastar(blind(),w=1)' --plan-file sas_plan < output
reading input... [t=0s]
Simplifying transitions... done!
done reading input! [t=0s]
building causal graph...done! [t=0s]
packing state variables...Variables: 6
Bytes per state: 4
done! [t=0s]
done initalizing global data [t=0s]
Conducting best first search with reopening closed nodes, (real) bound = 2147483647
Initializing blind heuristic...
f = 1 [1 evaluated, 0 expanded, t=0s, 6232 KB]
Best heuristic value: 1 [g=0, 1 evaluated, 0 expanded, t=0s, 6232 KB]
f = 2 [14 evaluated, 1 expanded, t=0s, 6232 KB]
f = 3 [62 evaluated, 14 expanded, t=0s, 6232 KB]
f = 4 [131 evaluated, 62 expanded, t=0s, 6232 KB]
f = 5 [398 evaluated, 131 expanded, t=0s, 6232 KB]
f = 6 [1003 evaluated, 398 expanded, t=0s, 6232 KB]
f = 7 [1770 evaluated, 1003 expanded, t=0s, 6232 KB]
f = 8 [3278 evaluated, 1770 expanded, t=0s, 6368 KB]
f = 9 [4588 evaluated, 3278 expanded, t=0s, 6368 KB]
f = 10 [7291 evaluated, 4588 expanded, t=0s, 6532 KB]
Solution found!
Actual search time: 0s [t=0s]
pickup la g1 a1 b1 (1)
pickup la g1 a2 b2 (1)
move g1 la lb (1)
drop lb g1 a1 b1 (1)
drop lb g1 a2 b2 (1)
move g1 lb la (1)
pickup la g1 a1 b3 (1)
move g1 la lb (1)
drop lb g1 a1 b3 (1)
move g1 lb la (1)
Plan length: 10 step(s).
Plan cost: 10
Initial state h value: 1.
Expanded 5879 state(s).
Reopened 0 state(s).
Evaluated 8869 state(s).
Evaluations: 8869
Generated 48315 state(s).
Dead ends: 0 state(s).
Expanded until last jump: 4588 state(s).
Reopened until last jump: 0 state(s).
Evaluated until last jump: 7291 state(s).
Generated until last jump: 37666 state(s).
Number of registered states: 8869
Search time: 0s
Total time: 0s
Solution found.
Peak memory: 6664 KB
