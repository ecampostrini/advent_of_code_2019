from collections import deque
from queue import Queue
from threading import Thread

from intcode import Intcode, load_program_from_file
from utils import get_absolute_path

INFINITY = 1e10
INPUT = get_absolute_path("day15.input")


# For debugging
def print_surface_size(surface):
    min_x = min_y = INFINITY
    max_x = max_y = -INFINITY
    for k in surface.keys():
        x, y = k
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)

    print("({}, {}) -> ({}, {})".format(min_x, max_y, max_x, min_y))


class RepairDroid(Intcode):
    def __init__(self, program):
        super(RepairDroid, self).__init__(program)
        self.in_queue = Queue()
        self.out_queue = Queue()
        self.finished = False

    def move(self, direction):
        self.in_queue.put(direction)
        return self.out_queue.get()

    def get(self):
        return self.in_queue.get()

    def put(self, item):
        self.out_queue.put(item)

    def run(self):
        while self.program[self.pc] != 99 and not self.finished:
            instruction = self.program[self.pc]
            self.step(instruction)


directions = [
    (1, 2, 0, 1),   # nord
    (4, 3, 1, 0),   # east
    (2, 1, 0, -1),  # sud
    (3, 4, -1, 0),  # west
]
elements = ['#', '.', 'O']
surface = {(0, 0): "."}
initial_oxigen = None


def get_min_dist(droid, surface, x, y, count):
    global initial_oxigen

    current_min = INFINITY
    for direction, reverse_direction, delta_x, delta_y in directions:
        if (x + delta_x, y + delta_y) in surface:
            continue

        move_result = droid.move(direction)
        surface[(x + delta_x, y + delta_y)] = elements[move_result]

        if move_result == 1:
            current_dist = get_min_dist(
                droid, surface, x + delta_x, y + delta_y, count + 1
            )
            if current_dist < current_min:
                current_min = current_dist
            droid.move(reverse_direction)

        if move_result == 2:
            initial_oxigen = (x + delta_x, y + delta_y)
            droid.move(reverse_direction)
            return count + 1
    return current_min


def spread_oxigen(surface, initial_oxigen):
    queue = deque([(initial_oxigen[0], initial_oxigen[1])])
    minutes = 0
    while len(queue):
        current = len(queue)
        filled_one = False
        while current > 0:
            x, y = queue.popleft()
            for _, _, delta_x, delta_y in directions:
                neighbour = (x + delta_x, y + delta_y)
                if surface.get(neighbour, 'X') == '.':
                    surface[neighbour] = 'O'
                    filled_one = True
                    queue.append(neighbour)
            current -= 1
        minutes += int(filled_one)
    return minutes


repair_droid = RepairDroid(load_program_from_file(INPUT))
thread_worker = Thread(target=repair_droid.run)
thread_worker.start()

min_dist = get_min_dist(repair_droid, surface, 0, 0, 0)
print("Part 1: ", min_dist)

repair_droid.finished = True
# Since the droid is in permaloop, sent him a dummy value so it
# checks once more the value of `finished` and leaves
repair_droid.in_queue.put("DUMMY")
thread_worker.join()

assert surface[initial_oxigen] == 'O'
print("Part 2: ", spread_oxigen(surface, initial_oxigen))
