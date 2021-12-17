#!/usr/bin/env python3
import re
from itertools import product


def x_in_boundary(min_x, max_x, v_x, n_steps):
    if v_x < n_steps:
        return min_x <= (v_x * (v_x + 1) // 2) <= max_x
    else:
        return min_x <= ((v_x + v_x - n_steps + 1) * n_steps // 2) <= max_x


def y_in_boundary(min_y, max_y, v_y, n_steps):
    return min_y <= ((v_y + v_y - n_steps + 1) * n_steps // 2) <= max_y


if __name__ == "__main__":
    with open("inputs/input17.txt", "r") as f:
        input_content = f.read()
    match = re.match(
        r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)",
        input_content
    )
    min_x, max_x, min_y, max_y = map(int, match.groups())
    y_velocity = abs(min_y) - 1
    highest_y = y_velocity * (y_velocity + 1) // 2
    print(f"Part A: {highest_y}")

    max_steps = abs(min_y) * 2
    possible_vectors = set()
    for n_steps in range(1, max_steps + 1):
        x_values = (v_x for v_x in range(max_x + 1) if x_in_boundary(min_x, max_x, v_x, n_steps))
        y_values = (v_y for v_y in range(min_y, y_velocity + 1) if y_in_boundary(min_y, max_y, v_y, n_steps))
        possible_vectors.update(product(x_values, y_values))
    print(f"Part B: {len(possible_vectors)}")
