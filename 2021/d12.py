#!/usr/bin/env python3

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class Node:
    name: str
    neighbours: Dict[str, 'Node'] = field(hash=False, compare=False, default_factory=dict)

    @property
    def is_large(self):
        return self.name.isupper()


def find_all_paths(start_node, end_node, cave_allowed_to_revisit=None):
    def explore(node, current_path, found_paths):
        for neighbour in node.neighbours.values():
            if neighbour is end_node:
                found_paths.append((*current_path, node, end_node))
            elif neighbour.is_large or neighbour not in current_path or \
                    (neighbour is cave_allowed_to_revisit and current_path.count(neighbour) < 2):
                explore(neighbour, (*current_path, node), found_paths)

    paths = []
    explore(start_node, [], paths)
    return paths


if __name__ == "__main__":
    with open("inputs/input12.txt", "r") as f:
        lines = f.read().splitlines()
    graph = {}
    for line in lines:
        a, b = line.split("-")
        node_a = graph.setdefault(a, Node(name=a, neighbours={}))
        node_b = graph.setdefault(b, Node(name=b, neighbours={}))
        node_a.neighbours[node_b.name] = node_b
        node_b.neighbours[node_a.name] = node_a

    paths_a = find_all_paths(graph["start"], graph["end"])
    answer_a = len(paths_a)
    print(f"Part A: {answer_a}")

    paths_b = set(
        tuple(path)
        for node in graph.values() if not node.is_large and node.name not in {"start", "end"}
        for path in find_all_paths(graph["start"], graph["end"], cave_allowed_to_revisit=node)
    )
    answer_b = len(paths_b)
    print(f"Part B: {answer_b}")

