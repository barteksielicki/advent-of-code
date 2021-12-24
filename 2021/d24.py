#!/usr/bin/env python3
import sys
from functools import lru_cache
from itertools import groupby


def split_steps(instructions):
    return [list(group) for k, group in groupby(instructions, lambda i: i.startswith("inp")) if not k]


@lru_cache(maxsize=None)
def check(w, x, y, z, step, part):
    global steps
    state = {"w": w, "x": x, "y": y, "z": z}
    if step == 1:
        print(f" {w}")
    for instruction in steps[step]:
        op, var1, var2 = instruction.split()
        val2 = state[var2] if var2.isalpha() else int(var2)
        if op == "add":
            state[var1] += val2
        elif op == "mul":
            state[var1] *= val2
        elif op == "div":
            state[var1] //= val2
        elif op == "mod":
            state[var1] %= val2
        elif op == "eql":
            state[var1] = int(state[var1] == val2)
    if step == 13:
        return str(w) if state["z"] == 0 else ""
    else:
        for w1 in range(9, 0, -1) if part == "1" else range(1, 10):
            output = check(w1, state["x"], state["y"], state["z"], step + 1, part)
            if output:
                return str(w) + output
        return ""


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"1", "2"}:
        sys.exit(f"Usage: {sys.argv[0]} <1,2>")
    part = sys.argv[1]
    with open("inputs/input24.txt", "r") as f:
        instructions = f.read().splitlines()
        steps = split_steps(instructions)
    answer_a = ""
    for w in range(9, 0, -1) if part == "1" else range(1, 10):
        print(w)
        output = check(w, 0, 0, 0, 0, part)
        if output:
            answer_a = output
            break
    print(f"Answer {part}: {answer_a}")
