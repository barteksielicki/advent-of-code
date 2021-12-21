#!/usr/bin/env python3
from collections import defaultdict
from itertools import cycle, islice


def take(iterable, n):
    return list(islice(iterable, n))


def play_part_1(p1_position, p2_position):
    dice = cycle(range(1, 101))
    p1_score = p2_score = 0
    dice_counter = 0
    while True:
        p1_position = ((p1_position + sum(take(dice, 3))) % 10) or 10
        dice_counter += 3
        p1_score += p1_position
        if p1_score >= 1000:
            break
        p2_position = ((p2_position + sum(take(dice, 3))) % 10) or 10
        p2_score += p2_position
        dice_counter += 3
        if p2_score >= 1000:
            break
    return min(p1_score, p2_score) * dice_counter


def play_part_2(p1_position, p2_position):
    n_universes = defaultdict(lambda: 0)
    n_universes[(0, p1_position, 0, p2_position, 0)] = 1
    round_outcomes = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

    def still_playing():
        return (
            (round_num, p1_position, p1_score, p2_position, p2_score)
            for (round_num, p1_position, p1_score, p2_position, p2_score), number in n_universes.items()
            if p1_score < 21 and p2_score < 21 and number > 0
        )
    universes_to_simulate = list(still_playing())
    player_1 = True
    rounds = 0
    while len(universes_to_simulate):
        for (round_num, p1_position, p1_score, p2_position, p2_score) in universes_to_simulate:
            n = n_universes[(round_num, p1_position, p1_score, p2_position, p2_score)]
            n_universes[(round_num, p1_position, p1_score, p2_position, p2_score)] = 0
            for round_sum, n_outcomes in round_outcomes.items():
                if player_1:
                    new_p1_position = ((p1_position + round_sum) % 10) or 10
                    new_p1_score = p1_score + new_p1_position
                    n_universes[(round_num + 1, new_p1_position, new_p1_score, p2_position, p2_score)] += n * n_outcomes
                else:
                    new_p2_position = ((p2_position + round_sum) % 10) or 10
                    new_p2_score = p2_score + new_p2_position
                    n_universes[(round_num + 1, p1_position, p1_score, new_p2_position, new_p2_score)] += n * n_outcomes
        player_1 = not player_1
        universes_to_simulate = list(still_playing())
        rounds += 1
    player_1_wins = sum(
        n for (round_num, p1_position, p1_score, p2_position, p2_score), n in n_universes.items()
        if p1_score >= 21
    )
    player_2_wins = sum(
        n for (round_num, p1_position, p1_score, p2_position, p2_score), n in n_universes.items()
        if p2_score >= 21
    )
    return max(player_1_wins, player_2_wins)


if __name__ == "__main__":
    with open("inputs/input21.txt", "r") as f:
        p1_position = int(f.readline().split()[-1])
        p2_position = int(f.readline().split()[-1])

    answer_a = play_part_1(p1_position, p2_position)
    print(f"Answer A: {answer_a}")

    answer_b = play_part_2(p1_position, p2_position)
    print(f"Answer B: {answer_b}")
