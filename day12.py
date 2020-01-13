from itertools import combinations
import re

from utils import get_absolute_path


class Moon:
    def __init__(self, x, y, z):
        self.position = (x, y, z)
        self.velocity = (0, 0, 0)

    def kinetic_energy(self):
        return sum([abs(x) for x in self.velocity])

    def potential_energy(self):
        return sum([abs(x) for x in self.position])

    def total_energy(self):
        return self.kinetic_energy() * self.potential_energy()

    def update_position(self):
        old_x, old_y, old_z = self.position
        vel_x, vel_y, vel_z = self.velocity
        self.position = (old_x + vel_x, old_y + vel_y, old_z + vel_z)

    def get_state(self):
        return self.position + self.velocity

    def __str__(self):
        px, py, pz = self.position
        vx, vy, vz = self.velocity
        return "pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>".format(
            px, py, pz, vx, vy, vz)


def apply_gravity(m1: Moon, m2: Moon):
    p1_x, p1_y, p1_z = m1.position
    p2_x, p2_y, p2_z = m2.position

    def get_delta(x, y):
        return 1 if x < y else -1 if x > y else 0

    delta_x = get_delta(p1_x, p2_x)
    delta_y = get_delta(p1_y, p2_y)
    delta_z = get_delta(p1_z, p2_z)

    v1_x, v1_y, v1_z = m1.velocity
    v2_x, v2_y, v2_z = m2.velocity
    m1.velocity = (v1_x + delta_x, v1_y + delta_y, v1_z + delta_z)
    m2.velocity = (v2_x - delta_x, v2_y - delta_y, v2_z - delta_z)


TEST_INPUT = get_absolute_path("day12.test.input")
INPUT = get_absolute_path("day12.input")
STEPS = 1000

input_regex = re.compile("\<x=(-?[0-9]+),\s*y=(-?[0-9]+),\s*z=(-?[0-9]+)\>")
with open(INPUT) as f:
    moons = []
    for line in f.readlines():
        m = input_regex.match(line)
        moons.append(Moon(int(m.group(1)), int(m.group(2)), int(m.group(3))))

    # for i in range(1, STEPS+1):
    #     # Update the velocities
    #     for m1, m2 in combinations(moons, 2):
    #         apply_gravity(m1, m2)

    #     # Update the positions
    #     for m in moons:
    #         m.update_position()

    #     # print("Step: {}".format(i))
    #     # [print(m) for m in moons]

    # total_energy = sum([m.total_energy() for m in moons])
    # print("Total energy: {}".format(total_energy))

    print("Part2")
    # The following solution is too slow, I still have to replace it with a proper one
    initial_states = [m.get_state() for m in moons]
    i = 1
    while True:
        # Update the velocities
        for m1, m2 in combinations(moons, 2):
            apply_gravity(m1, m2)

        # Update the positions
        for m in moons:
            m.update_position()

        new_states = [m.get_state() for m in moons]
        if initial_states == new_states:
            print(i)
            break
        if moons[0].velocity == (
                0, 0, 0) and moons[1].velocity == (
                0, 0, 0) and moons[2].velocity == (
                0, 0, 0) and moons[3].velocity == (
                0, 0, 0):
            print(i)

        if i % 1000000 == 0:
            print(i)

        i += 1
