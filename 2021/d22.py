#!/usr/bin/env python3
import re
from collections import defaultdict
from dataclasses import dataclass
from more_itertools import pairwise


@dataclass(frozen=True)
class Cuboid:
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int
    turn_on: bool
    priority: int

    @classmethod
    def parse(cls, text, priority):
        operation, coords = text.split()
        min_x, max_x, min_y, max_y, min_z, max_z = map(int, re.findall(r"-?\d+", coords))
        return cls(min_x, max_x + 1, min_y, max_y + 1, min_z, max_z + 1, operation == "on", priority)


def get_sectors(cuboids, axis):
    checkpoints = defaultdict(lambda: {"starts": set(), "ends": set()})
    for cuboid in cuboids:
        if axis == "x":
            checkpoints[cuboid.min_x]["starts"].add(cuboid)
            checkpoints[cuboid.max_x]["ends"].add(cuboid)
        elif axis == "y":
            checkpoints[cuboid.min_y]["starts"].add(cuboid)
            checkpoints[cuboid.max_y]["ends"].add(cuboid)
        elif axis == "z":
            checkpoints[cuboid.min_z]["starts"].add(cuboid)
            checkpoints[cuboid.max_z]["ends"].add(cuboid)
        else:
            raise ValueError(axis)

    overlapping_cuboids = set()
    sectors = []
    for start, end in pairwise(sorted(checkpoints)):
        overlapping_cuboids.update(checkpoints[start]["starts"])
        overlapping_cuboids.difference_update(checkpoints[start]["ends"])
        sectors.append((start, end, overlapping_cuboids.copy()))
    return sectors


def sum_volume_on(cuboids):
    x_sectors = get_sectors(cuboids, "x")
    y_sectors = get_sectors(cuboids, "y")
    z_sectors = get_sectors(cuboids, "z")
    volume = 0
    for min_x, max_x, x_cuboids in x_sectors:
        for min_y, max_y, y_cuboids in y_sectors:
            x_y_cuboids = x_cuboids & y_cuboids
            if x_y_cuboids:
                for min_z, max_z, z_cuboids in z_sectors:
                    x_y_z_cuboids = x_y_cuboids & z_cuboids
                    if x_y_z_cuboids:
                        final_cuboid = sorted(x_y_z_cuboids, key=lambda c: c.priority)[-1]
                        if final_cuboid.turn_on:
                            volume += abs(max_x - min_x) * abs(max_y - min_y) * abs(max_z - min_z)
    return volume


if __name__ == "__main__":
    with open("inputs/input22.txt", "r") as f:
        cuboids = [Cuboid.parse(line, i) for i, line in enumerate(f.read().splitlines())]

    answer_a = sum_volume_on([
        c for c in cuboids
        if -50 <= c.min_x and c.max_x <= 50 and -50 <= c.min_y and c.max_y <= 50 and -50 <= c.min_z and c.max_z <= 50
    ])
    print(f"Answer A: {answer_a}")

    answer_b = sum_volume_on(cuboids)
    print(f"Answer B: {answer_b}")
