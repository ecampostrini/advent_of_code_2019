from collections import defaultdict, deque, namedtuple
from functools import reduce
import re

INPUT = "/home/ecampostrini/advent_of_code/repo/day14.input"
TEST_INPUT = "/home/ecampostrini/advent_of_code/repo/day14.test.input"


class Reaction(namedtuple("Reaction", ["name", "qtty", "dependencies"])):
    def add_dependency(self, name: str, qtty: int):
        self.dependencies.append((name, qtty))

    def __str__(self):
        deps = ", ".join(["{1} {0}".format(d[0], d[1]) for d in self.dependencies])
        return "{0} => {1} {2}".format(deps, self.qtty, self.name)


def is_terminal(name: str) -> bool:
    if name not in reactions:
        raise RuntimeError("Chem name not found in reactions: {}".format(name))

    _, _, deps = reactions[name]
    if len(deps) == 1 and deps[0][0] == "ORE":
        return True
    return False


def get_ore_for_terminal(name, qtty):
    _, min_qtty, deps = reactions[name]
    multiplier = (qtty // min_qtty) + int(qtty % min_qtty != 0)
    # Since it's a termina the only dependency it has is an ORE
    _, ore_qtty = deps[0]
    return ore_qtty * multiplier


def normalize(name: str, qtty: int):
    reserve = defaultdict(int)
    terminals = defaultdict(int)
    non_terminals = defaultdict(int)

    non_terminals[name] = qtty
    while len(non_terminals):
        name, desired_qtty = non_terminals.popitem()

        if name not in reactions:
            raise RuntimeError("Didn't find reaction for chemical: {}".format(name))

        if reserve[name] >= desired_qtty:
            reserve[name] -= desired_qtty
            continue
        else:
            desired_qtty -= reserve[name]
            reserve[name] = 0

        _, reaction_qtty, reaction_deps = reactions[name]
        multiplier = (desired_qtty // reaction_qtty) + int(
            desired_qtty % reaction_qtty != 0
        )
        for d_name, d_qtty in reaction_deps:
            if is_terminal(d_name):
                terminals[d_name] += multiplier * d_qtty
            else:
                non_terminals[d_name] += multiplier * d_qtty
        reserve[name] = reaction_qtty * multiplier - desired_qtty

    acc = 0
    for k, v in terminals.items():
        # print("{} {}".format(k, v))
        acc += get_ore_for_terminal(k, v)
    return acc


chem_qtty_regex = r"([0-9]+)\s+([A-Z]+)"


def load_reactions(filename: str):
    reactions = {}
    with open(filename) as f:
        for line in f.readlines():
            dependencies, chem = [s.strip() for s in line.split("=>")]
            dependencies = [d.strip() for d in dependencies.split(",")]

            # Create the reaction
            chem_qtty, chem_name = [m for m in re.match(chem_qtty_regex, chem).groups()]
            reaction = Reaction(name=chem_name, qtty=int(chem_qtty), dependencies=[])

            # Add the dependencies
            for dep in dependencies:
                dep_qtty, dep_name = [
                    m for m in re.match(chem_qtty_regex, dep).groups()
                ]
                reaction.add_dependency(dep_name, int(dep_qtty))

            # Add the reaction to the map
            reactions[chem_name] = reaction
        return reactions


reactions = load_reactions(INPUT)
# For debugging
# for reaction in reactions.values():
#     print(reaction)

print("Part1: {}".format(normalize("FUEL", 1)))


def binary_search(left, right):
    while left <= right:
        mid = (left + right) // 2
        ores = normalize("FUEL", mid)

        if ores == ONE_TRILLON_ORE:
            return mid, ores
        if ores < ONE_TRILLON_ORE:
            left = mid + 1
        else:
            right = mid - 1
    return right, normalize("FUEL", right)


ONE_TRILLON_ORE = int(1e12)
fuel_qtty = 1
while ONE_TRILLON_ORE - normalize("FUEL", fuel_qtty) > 0:
    fuel_qtty = fuel_qtty * 2

left = fuel_qtty // 2 if fuel_qtty != 1 else 1
right = fuel_qtty

fuel_qtty, ores = binary_search(left, right)
print("Part2: {}".format(fuel_qtty))
# print("Actual ore required: {}".format(ores))
