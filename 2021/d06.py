#!/usr/bin/env python3

import functools


@functools.lru_cache(maxsize=None)
def offsprings_count(timer_state, days_left):
    if timer_state >= days_left:
        return 0
    return 1 + offsprings_count(6, days_left - timer_state - 1) + offsprings_count(8, days_left - timer_state - 1)


if __name__ == "__main__":
    with open("inputs/input06.txt", "r") as f:
        fishes = [int(n) for n in f.readline().split(",")]

    offsprings_a = [offsprings_count(fish_timer, 80) for fish_timer in fishes]
    answer_a = len(fishes) + sum(offsprings_a)
    print(f"Part A: {answer_a}")

    offsprings_b = [offsprings_count(fish_timer, 256) for fish_timer in fishes]
    answer_b = len(fishes) + sum(offsprings_b)
    print(f"Part B: {answer_b}")
