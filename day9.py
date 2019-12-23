from intcode import Intcode

INPUT = "day9.input"
TEST_INPUT = "day9.test.input"

with open(INPUT) as f:
    program = [int(n) for n in f.readline().split(",")]
    intcode = Intcode(program)
    intcode.run()
