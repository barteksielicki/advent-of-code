#!/usr/bin/env python3
import heapq
import sys
from collections import defaultdict
from functools import lru_cache


@lru_cache(maxsize=None)
def neighbours(node, max_x, max_y):
    x, y = node
    neighbours = set()
    if x > 0:
        neighbours.add((x - 1, y))
    if x < max_x:
        neighbours.add((x + 1, y))
    if y > 0:
        neighbours.add((x, y - 1))
    if y < max_y:
        neighbours.add((x, y + 1))
    return neighbours


def extend_level_map(level_map, size_x, size_y):
    new_level_map = level_map.copy()
    for y in range(size_y * 5):
        for x in range(size_x * 5):
            x_sector = x // size_x
            y_sector = y // size_y
            if x_sector or y_sector:
                old_value = level_map[(x % size_x, y % size_y)]
                new_value = old_value + x_sector + y_sector
                new_level_map[(x, y)] = new_value if new_value < 10 else new_value - 9
    return new_level_map


# def bellman_ford(graph, max_x, max_y):
#     distance = defaultdict(lambda: sys.maxsize)
#     distance[(0, 0)] = 0
#     for _ in range(len(graph)):
#         for node_a in graph:
#             for node_b in neighbours(node_a, max_x, max_y):
#                 if distance[node_b] > distance[node_a] + graph[node_b]:
#                     distance[node_b] = distance[node_a] + graph[node_b]
#     return distance


def dijkstra(graph, max_x, max_y):
    distance = defaultdict(lambda: sys.maxsize)
    distance[(0, 0)] = 0
    heap = [(0, (0, 0))]
    heapq.heapify(heap)
    while len(heap):
        dist_a, node_a = heapq.heappop(heap)
        for node_b in neighbours(node_a, max_x, max_y):
            if distance[node_b] > distance[node_a] + graph[node_b]:
                distance[node_b] = distance[node_a] + graph[node_b]
                heapq.heappush(heap, (distance[node_b], node_b))
    return distance


if __name__ == "__main__":
    with open("inputs/input15.txt", "r") as f:
        lines = f.read().splitlines()
    level_map = {(x, y): int(level) for y, row in enumerate(lines) for x, level in enumerate(row)}
    max_x, max_y = len(lines[0]) - 1, len(lines) - 1

    distance_map_a = dijkstra(level_map, max_x, max_y)
    answer_a = distance_map_a[(max_x, max_y)]
    print(f"Part A: {answer_a}")

    extended_level_map = extend_level_map(level_map, max_x + 1, max_y + 1)
    extended_max_x = 5 * (max_x + 1) - 1
    extended_max_y = 5 * (max_y + 1) - 1
    distance_map_b = dijkstra(extended_level_map, extended_max_x, extended_max_y)
    answer_b = distance_map_b[(extended_max_x, extended_max_y)]
    print(f"Part B: {answer_b}")
