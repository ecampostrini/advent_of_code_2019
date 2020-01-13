from math import gcd

from utils import get_absolute_path


def count_detections(station, asteroids):
    blocked_directions = set()

    for target in asteroids:
        if target == station:
            continue
        x, y = station[0] - target[0], station[1] - target[1]
        divisor = gcd(x, y)
        direction = (x // divisor, y // divisor)
        if direction not in blocked_directions:
            blocked_directions.add(direction)

    return len(blocked_directions)


INPUT = get_absolute_path("day10.input")
TEST_INPUT = get_absolute_path("day10.test.input")

with open(TEST_INPUT) as f:
    asteroids = []
    i = j = 0
    for line in f.readlines():
        for cell in [c for c in line.rstrip("\n")]:
            if cell == '#':
                asteroids.append((j, i))
            j += 1
        j = 0
        i += 1

    max_detection = -1
    best_spot = None
    for asteroid in asteroids:
        count = count_detections(asteroid, asteroids)
        if count > max_detection:
            max_detection = count
            best_spot = asteroid

    print("Part 1: ", max_detection)
    # print(best_spot)
