#!/usr/bin/env python3
import math
import re
from itertools import product, chain


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
    v_x_that_converge_to_target = [x_vel for x_vel in range(max_x) if min_x <= (x_vel * (x_vel + 1) // 2) <= max_x]
    for n_steps in range(1, max_steps + 1):
        min_v_x = math.ceil((min_x / n_steps) + ((n_steps - 1) / 2))
        max_v_x = math.floor((max_x / n_steps) + ((n_steps - 1) / 2))
        x_values = chain(
            (v_x for v_x in range(min_v_x, max_v_x + 1) if v_x >= n_steps),
            (v_x for v_x in v_x_that_converge_to_target if v_x < n_steps)
        )
        min_v_y = math.ceil((min_y / n_steps) + ((n_steps - 1) / 2))
        max_v_y = math.floor((max_y / n_steps) + ((n_steps - 1) / 2))
        y_values = range(min_v_y, max_v_y + 1)
        possible_vectors.update(product(x_values, y_values))
    print(f"Part B: {len(possible_vectors)}")
