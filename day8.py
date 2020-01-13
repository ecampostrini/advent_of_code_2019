from utils import get_absolute_path

WIDTH = 25
HEIGHT = 6
LAYER_SIZE = WIDTH * HEIGHT

INPUT_PATH = get_absolute_path("day8.input")
TEST_INPUT_PATH = get_absolute_path("day8.test.input")

INPUT2_PATH = INPUT_PATH
TEST_INPUT2_PATH = get_absolute_path("day8_part2.test.input")


def part1(input):
    min_zeros = 999999999999
    result = 0
    zeros = ones = twos = 0

    for i in range(0, len(input)):
        if (i + 1) % LAYER_SIZE == 0:
            if zeros < min_zeros:
                result = ones * twos
                min_zeros = zeros
            zeros = ones = twos = 0

        n = input[i]
        if n == 0:
            zeros += 1
        if n == 1:
            ones += 1
        if n == 2:
            twos += 1

    print("Part1: {}".format(result))


def part2(input):
    BLACK = 0
    WHITE = 1
    TRANSPARENT = 2

    result = [TRANSPARENT] * LAYER_SIZE
    for i in range(0, len(input)):
        idx = i % LAYER_SIZE
        if result[idx] == TRANSPARENT:
            result[idx] = input[i]

    for i in range(0, HEIGHT):
        r = [
            str(n)
            if n == WHITE else ' ' for n in result
            [i * WIDTH: i * WIDTH + WIDTH]]
        print("".join(r))


# with open(INPUT_PATH) as f:
#     input = [int(n) for n in f.readline().rstrip("\n")]
#     part1(input)

with open(INPUT2_PATH) as f:
    input = [int(n) for n in f.readline().rstrip('\n')]
    part2(input)
