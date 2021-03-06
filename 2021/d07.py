#!/usr/bin/env python3


def fuel_cost_a(positions, target):
    return sum(abs(pos - target) for pos in positions)


def fuel_cost_b(positions, target):
    def distance_cost(dist):
        return dist * (dist + 1) / 2
    return sum(distance_cost(abs(pos - target)) for pos in positions)


if __name__ == "__main__":
    with open("inputs/input07.txt", "r") as f:
        crabs = [int(n) for n in f.read().split(",")]

    fuel_costs_a = [fuel_cost_a(crabs, target) for target in range(min(crabs), max(crabs))]
    answer_a = min(fuel_costs_a)
    print(f"Part A: {answer_a}")

    fuel_costs_b = [fuel_cost_b(crabs, target) for target in range(min(crabs), max(crabs))]
    answer_b = min(fuel_costs_b)
    print(f"Part B: {answer_b}")
