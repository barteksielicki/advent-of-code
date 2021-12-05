#!/usr/bin/env python3

import re


def decode_input_line(line):
    match = re.match(r"(\d+)-(\d+) (\w): (\w+)", line)
    a, b, letter, password = match.groups()
    return int(a), int(b), letter, password


if __name__ == "__main__":
    with open("inputs/input02.txt", "r") as f:
        lines = f.readlines()
    correct_passwords_part_a = 0
    correct_passwords_part_b = 0
    for line in lines:
        a, b, letter, password = decode_input_line(line)
        if a <= password.count(letter) <= b:
            correct_passwords_part_a += 1
        if (password[a - 1] == letter) ^ (password[b - 1] == letter):
            correct_passwords_part_b += 1
    print(f"Part A: {correct_passwords_part_a}")
    print(f"Part B: {correct_passwords_part_b}")
