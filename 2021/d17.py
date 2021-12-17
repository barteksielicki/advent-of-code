#!/usr/bin/env python3
import re

if __name__ == "__main__":
    with open("inputs/input17.txt", "r") as f:
        input_content = f.read()
    match = re.match(
        r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)",
        input_content
    )
    min_x, max_x, min_y, max_y = map(int, match.groups())
    x_velocity_array = [i * (i + 1) // 2 for i in range(30)]
    y_velocity = abs(min_y) - 1
    highest_y = y_velocity * (y_velocity + 1) // 2
    print(f"Part A: {highest_y}")
