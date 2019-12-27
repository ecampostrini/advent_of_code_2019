from enum import IntEnum


def load_program_from_file(filename):
    with open(filename) as f:
        program = [int(n) for n in f.readline().split(",")]
    return program


class OpCode(IntEnum):
    ADD = 1
    MULT = 2
    READ = 3
    WRITE = 4
    ZERO = 5
    NOT_ZERO = 6
    LESS = 7
    EQUAL = 8
    RELATIVE_BASE = 9


class Intcode:
    @classmethod
    def from_file(cls, filename):
        return cls(load_program_from_file(filename))

    @staticmethod
    def parse_modes(instruction):
        instruction = "0" * (5 - len(instruction)) + instruction
        return [int(instruction[2]), int(instruction[1]), int(instruction[0])]

    def __init__(self, program):
        self.program = program.copy()
        self.memory = {}
        self.relative_base = 0
        self.pc = 0

    def store(self, mode, pos, val):
        try:
            if mode == 0:  # position mode
                pos = self.program[pos]
                self.program[pos] = val
            elif mode == 2:  # relative mode
                pos = self.program[pos] + self.relative_base
                self.program[pos] = val
            else:
                raise RuntimeError(
                    "Called store with unsupported mode: {}".format(mode))
        except IndexError:
            self.memory[pos] = val

    def load(self, mode, pos):
        try:
            if mode == 0:  # position mode
                return self.program[pos]
            if mode == 1:  # immediate mode
                return pos
            if mode == 2:  # relative mode
                pos = self.relative_base + pos
                if pos < 0:
                    raise RuntimeError(
                        "Called load with invalid address: {}".format(pos))
                return self.program[pos]
            raise RuntimeError("Called load with invalid mode: {}".format(mode))
        except IndexError:
            return self.memory.get(pos, 0)

    def get(self):
        return int(input("> "))

    def put(self, data):
        print(data)

    def step(self, instruction):
        program = self.program
        op_code = instruction % 10
        if op_code == OpCode.ADD:
            m1, m2, m3 = Intcode.parse_modes(str(instruction))
            op1 = self.load(m1, program[self.pc+1])
            op2 = self.load(m2, program[self.pc+2])
            ret = op1 + op2
            self.store(m3, self.pc+3, ret)
            self.pc += 4
        elif op_code == OpCode.MULT:
            m1, m2, m3 = Intcode.parse_modes(str(instruction))
            op1 = self.load(m1, program[self.pc+1])
            op2 = self.load(m2, program[self.pc+2])
            ret = op1 * op2
            self.store(m3, self.pc+3, ret)
            self.pc += 4
        elif op_code == OpCode.READ:
            data = self.get()
            m1, *_ = Intcode.parse_modes(str(instruction))
            self.store(m1, self.pc + 1, data)
            self.pc += 2
        elif op_code == OpCode.WRITE:
            m1, *_ = Intcode.parse_modes(str(instruction))
            value = self.load(m1, program[self.pc+1])
            self.put(value)
            self.pc += 2
        elif op_code == OpCode.ZERO:
            m1, m2, m3 = Intcode.parse_modes(str(instruction))
            op1 = self.load(m1, program[self.pc + 1])
            op2 = self.load(m2, program[self.pc + 2])
            self.pc = op2 if op1 != 0 else self.pc + 3
        elif op_code == OpCode.NOT_ZERO:
            m1, m2, m3 = Intcode.parse_modes(str(instruction))
            op1 = self.load(m1, program[self.pc + 1])
            op2 = self.load(m2, program[self.pc + 2])
            self.pc = op2 if op1 == 0 else self.pc + 3
        elif op_code == OpCode.LESS:
            m1, m2, m3 = Intcode.parse_modes(str(instruction))
            op1 = self.load(m1, program[self.pc+1])
            op2 = self.load(m2, program[self.pc+2])
            ret = 1 if op1 < op2 else 0
            self.store(m3, self.pc+3, ret)
            self.pc += 4
        elif op_code == OpCode.EQUAL:
            m1, m2, m3 = Intcode.parse_modes(str(instruction))
            op1 = self.load(m1, program[self.pc+1])
            op2 = self.load(m2, program[self.pc+2])
            ret = 1 if op1 == op2 else 0
            self.store(m3, self.pc+3, ret)
            self.pc += 4
        elif op_code == OpCode.RELATIVE_BASE:
            m1, *_ = Intcode.parse_modes(str(instruction))
            op1 = self.load(m1, program[self.pc+1])
            self.relative_base += op1
            self.pc += 2
        else:
            raise RuntimeError("Invalid OPCODE: {}".format(op_code))

    def run(self):
        while self.program[self.pc] != 99:
            instruction = self.program[self.pc]
            self.step(instruction)
