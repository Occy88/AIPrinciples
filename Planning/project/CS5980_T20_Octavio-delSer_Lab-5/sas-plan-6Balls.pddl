*** processed args: Namespace(alias=None, build='release32', components=['translate', 'preprocess', 'search'], filenames=['../../domains/gripper.pddl', '../../generator/gripper/states/state_0'], plan_file='sas_plan', planner_args=['../../domains/gripper.pddl', '../../generator/gripper/states/state_0', '--search', 'wastar(blind(),w=1)'], preprocess=False, preprocess_input='output.sas', preprocess_options=[], run_all=False, run_search=False, search_input='output', search_options=['--search', 'wastar(blind(),w=1)'], show_aliases=False, translate=False, translate_inputs=['../../domains/gripper.pddl', '../../generator/gripper/states/state_0'], translate_options=[])
INFO     Running translator.
INFO     callstring: /usr/bin/python /home/c4r4mel/PycharmProjects/AIPrinciples/Planning/project/solver/fd-stripped/builds/release32/bin/translate/translate.py ../../domains/gripper.pddl ../../generator/gripper/states/state_0
Parsing...
Parsing: [0.000s CPU, 0.001s wall-clock]
Normalizing task... [0.000s CPU, 0.000s wall-clock]
Instantiating...
Generating Datalog program... [0.000s CPU, 0.000s wall-clock]
Normalizing Datalog program...
Normalizing Datalog program: [0.000s CPU, 0.001s wall-clock]
Preparing model... [0.000s CPU, 0.000s wall-clock]
Generated 22 rules.
Computing model... [0.010s CPU, 0.006s wall-clock]
500 relevant atoms
349 auxiliary atoms
849 final queue length
1296 total queue pushes
Completing instantiation... [0.010s CPU, 0.009s wall-clock]
Instantiating: [0.020s CPU, 0.017s wall-clock]
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
Processing axioms: [0.000s CPU, 0.001s wall-clock]
Translating task: [0.010s CPU, 0.009s wall-clock]
132 effect conditions simplified
0 implied preconditions added
Detecting unreachable propositions...
0 operators removed
7 propositions removed
Detecting unreachable propositions: [0.000s CPU, 0.001s wall-clock]
Translator variables: 9
Translator derived variables: 0
Translator facts: 81
Translator goal facts: 7
Translator mutex groups: 7
Translator total mutex groups size: 77
Translator operators: 374
Translator axioms: 0
Translator task size: 2064
Translator peak memory: 20332 KB
Writing output... [0.000s CPU, 0.002s wall-clock]
Done! [0.030s CPU, 0.033s wall-clock]
INFO     Running preprocessor (release32).
INFO     callstring: /home/c4r4mel/PycharmProjects/AIPrinciples/Planning/project/solver/fd-stripped/builds/release32/bin/preprocess < output.sas
Building causal graph...
The causal graph is not acyclic.
9 variables of 9 necessary
0 of 7 mutex groups necessary.
374 of 374 operators necessary.
0 of 0 axiom rules necessary.
Building domain transition graphs...
solveable in poly time 0
Building successor generator...
Preprocessor facts: 81
Preprocessor derived variables: 0
Preprocessor task size: 1987
Writing output...
done

INFO     Running search (release32).
INFO     search executable: /home/c4r4mel/PycharmProjects/AIPrinciples/Planning/project/solver/fd-stripped/builds/release32/bin/downward
INFO     callstring: /home/c4r4mel/PycharmProjects/AIPrinciples/Planning/project/solver/fd-stripped/builds/release32/bin/downward --search 'wastar(blind(),w=1)' --plan-file sas_plan < output
reading input... [t=0s]
Simplifying transitions... done!
done reading input! [t=0s]
building causal graph...done! [t=0s]
packing state variables...Variables: 9
Bytes per state: 4
done! [t=0s]
done initalizing global data [t=0s]
Conducting best first search with reopening closed nodes, (real) bound = 2147483647
Initializing blind heuristic...
f = 1 [1 evaluated, 0 expanded, t=0s, 6364 KB]
Best heuristic value: 1 [g=0, 1 evaluated, 0 expanded, t=0s, 6364 KB]
f = 2 [23 evaluated, 1 expanded, t=0s, 6364 KB]
f = 3 [173 evaluated, 23 expanded, t=0s, 6364 KB]
f = 4 [545 evaluated, 173 expanded, t=0s, 6364 KB]
f = 5 [1835 evaluated, 545 expanded, t=0s, 6496 KB]
f = 6 [7795 evaluated, 1835 expanded, t=0s, 6760 KB]
f = 7 [14685 evaluated, 7795 expanded, t=0.02s, 7104 KB]
f = 8 [43855 evaluated, 14685 expanded, t=0.02s, 8660 KB]
f = 9 [90365 evaluated, 43855 expanded, t=0.08s, 10892 KB]
f = 10 [230915 evaluated, 90365 expanded, t=0.2s, 17384 KB]
f = 11 [510305 evaluated, 230915 expanded, t=0.54s, 30284 KB]
f = 12 [1229495 evaluated, 510305 expanded, t=1.38s, 63096 KB]
f = 13 [2260295 evaluated, 1229495 expanded, t=3.48s, 110540 KB]
f = 14 [3914387 evaluated, 2260295 expanded, t=6.42s, 189604 KB]
f = 15 [6635629 evaluated, 3914387 expanded, t=11.42s, 324480 KB]
f = 16 [11424711 evaluated, 6635629 expanded, t=19.96s, 520344 KB]
f = 17 [17071109 evaluated, 11424711 expanded, t=35.7s, 793616 KB]
f = 18 [26118227 evaluated, 17071109 expanded, t=56s, 1296220 KB]
Solution found!
Actual search time: 68.84s [t=68.84s]
pickup la g1 a1 b1 (1)
pickup la g1 a2 b2 (1)
move g1 la lb (1)
drop lb g1 a1 b1 (1)
drop lb g1 a2 b2 (1)
move g1 lb la (1)
pickup la g1 a1 b3 (1)
pickup la g1 a2 b4 (1)
move g1 la lb (1)
drop lb g1 a1 b3 (1)
drop lb g1 a2 b4 (1)
move g1 lb la (1)
pickup la g1 a1 b5 (1)
pickup la g1 a2 b6 (1)
move g1 la lb (1)
drop lb g1 a1 b5 (1)
drop lb g1 a2 b6 (1)
move g1 lb la (1)
Plan length: 18 step(s).
Plan cost: 18
Initial state h value: 1.
Expanded 21337258 state(s).
Reopened 0 state(s).
Evaluated 32114079 state(s).
Evaluations: 32114079
Generated 246356690 state(s).
Dead ends: 0 state(s).
Expanded until last jump: 17071109 state(s).
Reopened until last jump: 0 state(s).
Evaluated until last jump: 26118227 state(s).
Generated until last jump: 197719862 state(s).
Number of registered states: 32114079
Search time: 68.84s
Total time: 68.84s
Solution found.
Peak memory: 1502120 KB
