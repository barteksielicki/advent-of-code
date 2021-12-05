#!/usr/bin/env python3
from itertools import chain


def parse_boards(input_lines):
    boards = []
    current_board = rows, cols = ([], [set() for _ in range(5)])
    for line in input_lines:
        if line == '':
            boards.append(current_board)
            current_board = rows, cols = ([], [set() for _ in range(5)])
            continue
        row_numbers = [int(n) for n in line.split()]
        rows.append(set(row_numbers))
        for i, n in enumerate(row_numbers):
            cols[i].add(n)
    return boards


def play_bingo(boards, numbers):
    winning_boards = []
    for number in numbers:
        boards_won_that_round = []
        for board in boards:
            rows, cols = board
            for lane in chain(rows, cols):
                lane.discard(number)
                if len(lane) == 0 and board not in boards_won_that_round:
                    boards_won_that_round.append(board)
        for board in boards_won_that_round:
            winning_boards.append((board, number))
            boards.remove(board)
    return winning_boards


if __name__ == "__main__":
    with open("inputs/input04.txt", "r") as f:
        numbers = [int(n) for n in f.readline().split(",")]
        f.readline()  # empty line
        boards = parse_boards(f.read().splitlines())

    winners = play_bingo(boards, numbers)

    (rows, cols), winning_number = winners[0]
    answer_a = winning_number * sum(sum(row) for row in rows)
    print(f"Part A: {answer_a}")

    (rows, cols), winning_number = winners[-1]
    answer_b = winning_number * sum(sum(row) for row in rows)
    print(f"Part B: {answer_b}")
