#!/usr/bin/env python3


def read_groups_for_a(input_lines):
    groups = []
    current_group = set()
    for line in input_lines:
        if not line:
            groups.append(current_group)
            current_group = set()
            continue
        current_group.update(set(line))
    groups.append(current_group)
    return groups


def read_groups_for_b(input_lines):
    groups = []
    current_group = None
    for line in input_lines:
        if not line:
            groups.append(current_group)
            current_group = None
            continue
        if current_group is None:
            current_group = set(line)
        else:
            current_group = current_group & set(line)
    groups.append(current_group)
    return groups


if __name__ == "__main__":
    with open("inputs/input06.txt", "r") as f:
        lines = f.read().splitlines()

    groups_a = read_groups_for_a(lines)
    part_a_answer = sum(len(group) for group in groups_a)
    print(f"Part A: {part_a_answer}")

    groups_b = read_groups_for_b(lines)
    part_b_answer = sum(len(group) for group in groups_b)
    print(f"Part B: {part_b_answer}")
