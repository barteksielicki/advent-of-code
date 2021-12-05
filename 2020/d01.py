#!/usr/bin/env python3

def find_two_that_sum(numbers, expected_sum):
    for i, a in enumerate(numbers):
        for b in numbers[i + 1:]:
            if a + b == expected_sum:
                return a, b


def find_three_that_sum(numbers, expected_sum):
    for i, a in enumerate(numbers):
        other_two = find_two_that_sum(numbers[i + 1:], expected_sum - a)
        if other_two:
            return a, *other_two


if __name__ == "__main__":
    with open("inputs/input01.txt", "r") as f:
        numbers = [int(line) for line in f]
    a, b = find_two_that_sum(numbers, 2020)
    print(f"Part A: {a} * {b} = {a * b}")
    a, b, c = find_three_that_sum(numbers, 2020)
    print(f"Part B: {a} * {b} * {c} = {a * b * c}")
