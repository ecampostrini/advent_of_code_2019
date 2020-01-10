from utils import get_absolute_path

from collections import defaultdict

INPUT_PATH = get_absolute_path("day6.input")
INPUT_TEST_PATH = get_absolute_path("day6_2.input.test")


lines = []
with open(INPUT_PATH) as f:
    lines = [l.rstrip('\n') for l in f]

''' First part '''


def follow(n, graph):
    if n not in graph:
        return 0
    s = 0
    for v in graph[n]:
        s = 1 + follow(v, graph)
    return s


graph = defaultdict(list)
for l in lines:
    a, b = l.split(")")
    graph[b].append(a)

total_sum = len(graph)
for k, v in graph.items():
    for n in v:
        total_sum += follow(n, graph)

print(total_sum)

''' Second part '''


def count_transfers(a, b, graph, path):
    if a in path:
        return 999999

    if a == b:
        return 0

    path.add(a)
    min_distance = 999999
    for nb in graph[a]:
        count = count_transfers(nb, b, graph, path)
        if count < min_distance:
            min_distance = count

    path.remove(a)
    return min_distance + 1


graph = defaultdict(list)
my_orbital = None
santas_orbital = None
for l in lines:
    a, b = l.split(")")
    graph[a].append(b)
    graph[b].append(a)

    if l.endswith("SAN"):
        santas_orbital = a
    elif l.endswith("YOU"):
        my_orbital = a

path = set()
total_tranfers = count_transfers(my_orbital, santas_orbital, graph, path)
print(total_tranfers)
