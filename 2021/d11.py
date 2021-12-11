#!/usr/bin/env python3
from itertools import product


def neighbours(y, x):
    return [
        (y + y_delta, x + x_delta) for y_delta, x_delta in product((-1, 0, 1), repeat=2)
        if 0 <= y + y_delta < 10 and 0 <= x + x_delta < 10
    ]


def bump_by_1(board):
    flashes = set()
    for y, row in enumerate(board):
        for x, level in enumerate(row):
            row[x] = level + 1
            if row[x] == 10:
                flashes.add((y, x))
    return flashes


def bump_neighbours_by_1(board, flashes):
    new_flashes = set()
    for y_f, x_f in flashes:
        for y_n, x_n in neighbours(y_f, x_f):
            if board[y_n][x_n] < 10:
                board[y_n][x_n] += 1
                if board[y_n][x_n] == 10:
                    new_flashes.add((y_n, x_n))
    return new_flashes


def decrease_to_0(board, tiles):
    for y, x in tiles:
        board[y][x] = 0


def perform_step(board):
    flashes_this_step = bump_by_1(board)
    new_flashes = flashes_this_step
    while new_flashes:
        new_flashes = bump_neighbours_by_1(board, new_flashes)
        flashes_this_step.update(new_flashes)
    decrease_to_0(board, flashes_this_step)
    return len(flashes_this_step)


def count_flashes(board, steps):
    counter = 0
    for step in range(steps):
        flashes_this_step = perform_step(board)
        counter += flashes_this_step
    return counter


def run_until_all_flash(board):
    steps = 0
    flashes_this_step = 0
    while flashes_this_step != 100:
        steps += 1
        flashes_this_step = perform_step(board)
    return steps


if __name__ == "__main__":
    with open("inputs/input11.txt", "r") as f:
        board = [[int(level) for level in row] for row in f.read().splitlines()]

    answer_a = count_flashes(board, steps=100)
    print(f"Part A: {answer_a}")

    remaining_steps = run_until_all_flash(board)
    answer_b = remaining_steps + 100
    print(f"Part B: {answer_b}")
