from utils import get_absolute_path

with open(get_absolute_path("day2.input")) as f:
    nums = [int(n) for n in f.readline().split(",")]

    def op(op_code, x_pos, y_pos):
        x, y = mem[x_pos], mem[y_pos]
        if op_code == 1:
            return x + y
        if op_code == 2:
            return x * y
        raise RuntimeError("Invalid op_code: {}".format(op_code))

    for i in range(0, 100):
        for j in range(0, 100):
            mem = nums.copy()
            mem[1] = i
            mem[2] = j
            idx = 0
            while True:
                if mem[idx] == 99:
                    break
                op_code, pos_a, pos_b, dest = mem[idx: idx + 4]
                mem[dest] = op(op_code, pos_a, pos_b)
                idx += 4
            if mem[0] == 19690720:
                print("Result: {}, {}".format(i, j))
                exit(0)
