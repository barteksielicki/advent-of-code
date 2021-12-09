#!/usr/bin/env python3

from collections import deque


def sum_local_mins(height_map):
    x_size = len(height_map[0])
    y_size = len(height_map)
    answer = 0
    for y, row in enumerate(height_map):
        for x, depth in enumerate(row):
            neighbours = set()
            if x > 0:
                neighbours.add(row[x - 1])
            if x < (x_size - 1):
                neighbours.add(row[x + 1])
            if y > 0:
                neighbours.add(height_map[y - 1][x])
            if y < (y_size - 1):
                neighbours.add(height_map[y + 1][x])
            if all(depth < n for n in neighbours):
                answer += (1 + depth)
    return answer


def flood_fill(height_map, y, x, y_size, x_size):
    basin_tiles = set()
    queue = deque()
    queue.append((y, x))
    while len(queue):
        y, x = queue.pop()
        if height_map[y][x] != 9:
            basin_tiles.add((y, x))
            height_map[y][x] = 9
            if x > 0:
                queue.append((y, x - 1))
            if x < (x_size - 1):
                queue.append((y, x + 1))
            if y > 0:
                queue.append((y - 1, x))
            if y < (y_size - 1):
                queue.append((y + 1, x))
    return len(basin_tiles)


def find_basins(height_map):
    x_size = len(height_map[0])
    y_size = len(height_map)
    basin_sizes = []
    for y, row in enumerate(height_map):
        for x, depth in enumerate(row):
            if depth != 9:
                basin_size = flood_fill(height_map, y, x, y_size, x_size)
                basin_sizes.append(basin_size)
    return [b for b in basin_sizes if b > 0]


if __name__ == "__main__":
    with open("inputs/input09.txt", "r") as f:
        lines = f.read().splitlines()
    height_map = [[int(digit) for digit in line] for line in lines]

    answer_a = sum_local_mins(height_map)
    print(f"Part A: {answer_a}")

    basin_sizes = find_basins(height_map)
    a, b, c = sorted(basin_sizes)[-3:]
    answer_b = a * b * c
    print(f"Part B: {answer_b}")
