#!/usr/bin/env python3

from math import floor, ceil


def decode_seat(boarding_pass):
    min_row = 0
    max_row = 127
    min_col = 0
    max_col = 7
    for c in boarding_pass[:7]:
        if c == "F":
            max_row -= floor((max_row - min_row) / 2)
        else:
            min_row += ceil((max_row - min_row) / 2)
    for c in boarding_pass[7:]:
        if c == "L":
            max_col -= floor((max_col - min_col) / 2)
        else:
            min_col += ceil((max_col - min_col) / 2)
    return min_row, min_col


if __name__ == "__main__":
    with open("inputs/input05.txt", "r") as f:
        lines = f.read().splitlines()

    taken_seats = sorted(row * 8 + col for row, col in (decode_seat(line) for line in lines))
    max_seat_id = taken_seats[-1]
    print(f"Part A: {max_seat_id}")

    for seat_a, seat_b in zip(taken_seats, taken_seats[1:]):
        if seat_b - seat_a == 2:
            print(f"Part B: {seat_a + 1}")
