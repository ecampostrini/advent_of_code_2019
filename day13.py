from time import sleep
from threading import Thread
import os
from copy import deepcopy
from queue import Queue

from intcode import Intcode, load_program_from_file
from state_dump import state

TEST_INPUT = "/home/esteban/training/advent_of_code/repo/day13.test.input"
INPUT = "/home/esteban/training/advent_of_code/repo/day13.input"
TILES = [' ', 'X', 'O', '\033[35m^\033[0m', '\033[32mo\033[0m']


def print_screen(score, screen):
    os.system("clear")
    print("Score: {}".format(score))
    for row in screen:
        print("".join(row))


class TileIntcode(Intcode):
    def __init__(self, program):
        super(TileIntcode, self).__init__(program)
        self.output = Queue()
        self.finished = False
        self.screen = [[' '] * 45 for _ in range(0, 23)]
        self.score = 0
        self.moves = []
        self.replay = []

    def get(self):
        print_screen(self.score, self.screen)
        if len(self.replay):
            val = self.replay.pop()
            sleep(0.005)
        else:
            val = input("Move> ")
        move = 0
        if val == 0 or val == '':
            move = 0
        if val == -1 or val == '\x1b[D':
            move = -1
        if val == 1 or val == '\x1b[C':
            move = 1

        self.moves.append(move)
        # print("The val: {}".format(val))
        return move

    def put(self, val):
        return self.output.put(val)

    def run(self):
        super(TileIntcode, self).run()
        self.finished = True

    def step(self, instruction):
        super(TileIntcode, self).step(instruction)


machine = TileIntcode(load_program_from_file(INPUT))
if len(state):
    machine.replay = deepcopy(state)
    machine.replay.reverse()
machine_thread = Thread(target=machine.run)
machine_thread.start()
out_channel = machine.output
retry = "yes"

while True:
    while not machine.finished:
        x, y, tile_id = out_channel.get(), out_channel.get(), out_channel.get()

        if (x, y) == (-1, 0):
            machine.score = tile_id
        else:
            machine.screen[y][x] = TILES[tile_id]
        # print_screen(machine.score, machine.screen)
    machine_thread.join()

    if (not out_channel.empty()):
        _, _, final_score = out_channel.get(), out_channel.get(), out_channel.get()
        print("You won !! Final score: {}".format(final_score))
        dump_state = input("Dump state? (yes/no): ")
        if dump_state == "yes":
            with open("/tmp/state_dump.py", "w") as f:
                f.write("state = {0}\n".format(str(machine.moves)))
        exit(0)

    retry = input("Retry (yes/no): ")
    try:
        drop_count = int(input("Drop the last nth moves: "))
    except ValueError:
        drop_count = 30

    dump_state = input("Dump state? (yes/no): ")
    if dump_state == "yes":
        with open("/tmp/state_dump.py", "w") as f:
            f.write("state = {0}\n".format(str(machine.moves)))

    if retry == "yes":
        moves = deepcopy(machine.moves[:-drop_count])
        moves.reverse()
        machine = TileIntcode(load_program_from_file(INPUT))
        machine.replay = deepcopy(moves)
        machine_thread = Thread(target=machine.run)
        machine_thread.start()
        out_channel = machine.output
    else:
        break

# print("Part1: {0}".format(len(result)))
