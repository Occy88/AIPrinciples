class InvalidDomainSintax(Exception):
    pass


class Domain:
    def __init__(self):
        pass


def clean_pddl_data(data):
    lines = data.split("\n")
    # get ridd of comments
    for i in range(len(lines)):
        lines[i] = lines[i].split(";")[0]
    data = ''.join(lines)
    data = data.strip()
    data = data.replace('\n', '')
    data = data.replace('\t', '')
    return data


def get_pddl_branches(data):
    """
    returns the next list of branches from a pddl style data string.
    e.g.:
    "(asdf (asdf) (asdf) (asdf))"
    => {"asdf" : ["(asdf), (asdf), (asdf)"]}
    """

    if not (data[0] == '(' and data[-1] == ')'):
        return data.split(maxsplit=1)
    s = data[1:-1]
    (firstWord, rest) = s.split(maxsplit=1)
    # print(firstWord)
    # get set of bracket enclosed arguments.
    if not rest[0] == '(':
        return (firstWord, rest)
    args = []
    t = 0
    base = 0
    found = False
    for i in range(len(rest)):
        if rest[i] == '(':
            found = True
            t += 1
        elif rest[i] == ')':
            t -= 1
        if t == 0 and found:
            found = False
            args.append(rest[base:i + 1])
            base = i + 1
        elif t == 0 and not found:
            base += 1
    # for a in args:
    #     print(a)
    return (firstWord, args)


def parse_action():
    pass


def parse_predicates():
    pass


def parse_requirements():
    pass


def parse_types():
    pass


def generate_pddl_dict(data):
    print(data)
    key, rest = get_pddl_branches(data)
    if type(rest) == str:
        return {key: rest}
    else:
        to_ret = {key: {}}
        for s in rest:
            d = generate_pddl_dict(s)
            for k in d.keys():
                if k not in to_ret[key]:
                    to_ret[key][k] = generate_pddl_dict(d[k])
                else:
                    nk, nr = get_pddl_branches(d[k])
                    print(nk, '|----|', nr)
                    to_ret[key][k][nk] = generate_pddl_dict(nr)
        return to_ret


def test_get_pddl_branches():
    print(generate_pddl_dict(clean_pddl_data(open('../depotsstrips/Depots.pddl').read())))


test_get_pddl_branches()
s = {'define':
         {'domain': 'Depot',
          ':requirements': ':typing',
          ':types': 'place locatable - objectdepot distributor - place    truck hoist surface - locatable    pallet crate - surface',
          ':predicates': {'at': '?x - locatable ?y - place',
                          'on': '?x - crate ?y - surface',
                          'in': '?x - crate ?y - truck',
                          'lifting': '?x - hoist ?y - crate',
                          'available': '?x - hoist',
                          'clear': '?x - surface'},
          ':action': 'Unload :parameters (?x - hoist ?y - crate ?z - truck ?p - place):precondition (and (at ?x ?p) (at ?z ?p) (available ?x) (in ?y ?z)):effect (and (not (in ?y ?z)) (not (available ?x)) (lifting ?x ?y))'}}
