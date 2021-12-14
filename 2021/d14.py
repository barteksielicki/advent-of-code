#!/usr/bin/env python3
from collections import Counter
from copy import deepcopy

from more_itertools import pairwise


# def grow_polymer(template, rules, n_steps):
#     polymer = template
#     for _ in range(n_steps):
#         new_polymer = polymer[:1]
#         for a, b in pairwise(polymer):
#             if (a, b) in rules:
#                 new_polymer.append(rules[(a, b)])
#             new_polymer.append(b)
#         polymer = new_polymer
#     return polymer


def grow_polymer_smart(template, rules, n_steps):
    symbols_counter = Counter(template)
    pairs_counter = Counter(pairwise(template))
    for _ in range(n_steps):
        new_pairs_counter = deepcopy(pairs_counter)
        for (a, b), c in rules.items():
            pair_occurences = pairs_counter[(a, b)]
            new_pairs_counter[(a, c)] += pair_occurences
            new_pairs_counter[(c, b)] += pair_occurences
            new_pairs_counter[(a, b)] -= pair_occurences
            symbols_counter[c] += pair_occurences
        pairs_counter = new_pairs_counter
    return symbols_counter


if __name__ == "__main__":
    with open("inputs/input14.txt", "r") as f:
        lines = f.read().splitlines()

    template = list(lines[0])
    rules = {tuple(pair): symbol for pair, symbol in (line.split(" -> ") for line in lines[2:])}

    symbols_counter = grow_polymer_smart(template, rules, 10)
    occurences = sorted(symbols_counter.values())
    answer_a = occurences[-1] - occurences[0]
    print(f"Part A: {answer_a}")

    symbols_counter = grow_polymer_smart(template, rules, 40)
    occurences = sorted(symbols_counter.values())
    answer_b = occurences[-1] - occurences[0]
    print(f"Part B: {answer_b}")
