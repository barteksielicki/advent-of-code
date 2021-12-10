#!/usr/bin/env python3

from collections import deque

BRACKET_PAIRS = {'(': ')', '[': ']', '{': '}', '<': '>'}
OPENING_BRACKETS = set(BRACKET_PAIRS.keys())
CLOSING_BRACKETS = set(BRACKET_PAIRS.values())
INVALID_BRACKET_POINTS = {')': 3, ']': 57, '}': 1197, '>': 25137}
COMPLETION_POINTS = {')': 1, ']': 2, '}': 3, '>': 4}


def invalid_points(line):
    stack = deque()
    for bracket in line:
        if bracket in OPENING_BRACKETS:
            stack.append(bracket)
        elif not len(stack) or bracket != BRACKET_PAIRS[stack.pop()]:
            return INVALID_BRACKET_POINTS[bracket]
    return 0


def completion_points(line):
    stack = deque()
    for bracket in line:
        if bracket in OPENING_BRACKETS:
            stack.append(bracket)
        else:
            stack.pop()
    points = 0
    while len(stack):
        closing_bracket = BRACKET_PAIRS[stack.pop()]
        points *= 5
        points += COMPLETION_POINTS[closing_bracket]
    return points


if __name__ == "__main__":
    with open("inputs/input10.txt", "r") as f:
        lines = f.read().splitlines()

    answer_a = sum(invalid_points(line) for line in lines)
    print(f"Part A: {answer_a}")

    valid_lines = [line for line in lines if not invalid_points(line)]
    completion_scores = sorted(
        filter(lambda score: score != 0, (completion_points(line) for line in valid_lines))
    )
    answer_b = completion_scores[(len(completion_scores) - 1) // 2]
    print(f"Part B: {answer_b}")
