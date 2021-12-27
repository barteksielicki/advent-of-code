#!/usr/bin/env python3


def move_cucumbers(board):
    moves = 0
    len_y = len(board)
    len_x = len(board[0])
    # east facing
    updated_tiles = set()
    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            if tile == ">" and (y, x) not in updated_tiles:
                dest_x = (x + 1) % len_x
                if board[y][dest_x] == "." and (y, dest_x) not in updated_tiles:
                    board[y][x] = "."
                    board[y][dest_x] = ">"
                    updated_tiles.update({(y, x), (y, dest_x)})
                    moves += 1
    # south facing
    updated_tiles = set()
    for y, row in enumerate(board):
        for x, tile in enumerate(row):
            if tile == "v" and (y, x) not in updated_tiles:
                dest_y = (y + 1) % len_y
                if board[dest_y][x] == "." and (dest_y, x) not in updated_tiles:
                    board[y][x] = "."
                    board[dest_y][x] = "v"
                    updated_tiles.update({(y, x), (dest_y, x)})
                    moves += 1
    return moves


if __name__ == "__main__":
    with open("inputs/input25.txt", "r") as f:
        board = [list(line) for line in f.read().splitlines()]

    steps = 1
    while move_cucumbers(board):
        steps += 1

    print(f"Answer A: {steps}")
