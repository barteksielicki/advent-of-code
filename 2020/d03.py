#!/usr/bin/env python3


def find_trees_by_slope(lines, slope_right, slope_down):
    pattern_width = len(lines[0])
    x_pos = 0
    trees = 0
    for line in lines[slope_down::slope_down]:
        x_pos += slope_right
        if line[x_pos % pattern_width] == "#":
            trees += 1
    return trees


if __name__ == "__main__":
    with open("inputs/input03.txt", "r") as f:
        lines = f.read().splitlines()
    part_a_trees = find_trees_by_slope(lines, 3, 1)
    print(f"Part A: {part_a_trees}")

    part_b_slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    part_b_product = 1
    for slope_right, slope_down in part_b_slopes:
        part_b_product *= find_trees_by_slope(lines, slope_right, slope_down)
    print(f"Part B: {part_b_product}")
