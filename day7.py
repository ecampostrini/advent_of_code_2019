from utils import get_absolute_path

from itertools import permutations


INPUT_PATH = get_absolute_path("day7.input")
TEST_INPUT_PATH = get_absolute_path("day7.input.test")


def parse_op(op_code):
    op_code = "0" * (4 - len(op_code)) + op_code
    return [int(op_code[0]), int(op_code[1]), int(op_code[2:])]


def addition(a, b):
    return a + b


def mult(a, b):
    return a * b


def load(mode, posi):
    return posi if mode != 0 or posi >= len(nums) else nums[posi]


with open(INPUT_PATH) as f:
    program = [int(n) for n in f.readline().split(",")]

    max_signal = -1
    for phase_setting in permutations("01234", 5):
        current_output = 0
        for amplifier in range(0, 5):
            has_phase_setting = False
            nums = program.copy()
            pc = 0
            while nums[pc] != 99:
                op_code = nums[pc]
                if op_code % 10 == 3:
                    data = int(
                        phase_setting[amplifier]) if not has_phase_setting else current_output
                    has_phase_setting = True
                    pos = nums[pc+1]
                    nums[pos] = data
                    pc += 2
                elif op_code % 10 == 4:
                    _, m1, _ = parse_op(str(op_code))
                    operand = load(m1, nums[pc+1])
                    current_output = operand
                    pc += 2
                elif op_code % 10 == 5:
                    m2, m1, _ = parse_op(str(op_code))
                    op1, op2 = load(m1, nums[pc+1]), load(m2, nums[pc+2])
                    pc = op2 if op1 != 0 else pc + 3
                elif op_code % 10 == 6:
                    m2, m1, _ = parse_op(str(op_code))
                    op1, op2 = load(m1, nums[pc+1]), load(m2, nums[pc+2])
                    pc = op2 if op1 == 0 else pc + 3
                elif op_code % 10 == 7:
                    m2, m1, _ = parse_op(str(op_code))
                    op1, op2, op3 = load(
                        m1, nums[pc+1]), load(m2, nums[pc+2]), nums[pc+3]
                    nums[op3] = 1 if op1 < op2 else 0
                    pc += 4
                elif op_code % 10 == 8:
                    m2, m1, _ = parse_op(str(op_code))
                    op1, op2, op3 = load(
                        m1, nums[pc+1]), load(m2, nums[pc+2]), nums[pc+3]
                    nums[op3] = 1 if op1 == op2 else 0
                    pc += 4
                else:
                    m2, m1, parsed_op = parse_op(str(op_code))
                    operation = addition if parsed_op == 1 else mult
                    op1, op2 = load(m1, nums[pc+1]), load(m2, nums[pc+2])
                    ret_pos = nums[pc+3]
                    result = operation(op1, op2)
                    nums[ret_pos] = result
                    pc += 4
        if current_output > max_signal:
            max_signal = current_output

    print(max_signal)
