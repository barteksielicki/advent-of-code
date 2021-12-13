#!/usr/bin/env python3


def fold(dots, axis, value):
    if axis == "x":
        return {(value - (x - value) if x > value else x, y) for x, y in dots}
    elif axis == "y":
        return {(x, value - (y - value) if y > value else y) for x, y in dots}


if __name__ == "__main__":
    with open("inputs/input13.txt", "r") as f:
        lines = f.read().splitlines()
    dots = set(
        (int(x), int(y)) for x, y in
        (line.split(",") for line in lines if "," in line)
    )
    fold_instructions = [
        (instruction[-1], int(value)) for instruction, value in
        (line.split("=") for line in lines if line.startswith("fold"))
    ]

    axis, value = fold_instructions.pop(0)
    dots = fold(dots, axis, value)
    answer_a = len(dots)
    print(f"Part A: {answer_a}")

    for axis, value in fold_instructions:
        dots = fold(dots, axis, value)
    print(f"Part B:")
    max_x = max(x for x, y in dots)
    max_y = max(y for x, y in dots)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print("#" if (x, y) in dots else ".", end=" ")
        print("")
