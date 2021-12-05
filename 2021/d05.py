#!/usr/bin/env python3
from collections import defaultdict


def parse_line(input_line):
    start, end = input_line.split(" -> ")
    x1, y1 = map(int, start.split(","))
    x2, y2 = map(int, end.split(","))
    return (x1, y1), (x2, y2)


if __name__ == "__main__":
    with open("inputs/input05.txt", "r") as f:
        input_lines = f.read().splitlines()

    danger_level = defaultdict(lambda: 0)
    lines = [parse_line(l) for l in input_lines]
    for (x1, y1), (x2, y2) in lines:
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                danger_level[(x1, y)] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                danger_level[(x, y1)] += 1

    answer_a = sum(level >= 2 for level in danger_level.values())
    print(f"Part A: {answer_a}")

    for (x1, y1), (x2, y2) in lines:
        if x1 != x2 and y1 != y2:
            for i in range(max(x1, x2) + 1 - min(x1, x2)):
                x_delta = i if x1 < x2 else -i
                y_delta = i if y1 < y2 else -i
                danger_level[(x1 + x_delta, y1 + y_delta)] += 1

    answer_b = sum(level >= 2 for level in danger_level.values())
    print(f"Part B: {answer_b}")
