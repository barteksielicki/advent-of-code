#!/usr/bin/env python3
import json
import math
from dataclasses import dataclass
from itertools import permutations
from typing import Optional


@dataclass
class Node:
    value: Optional[int] = None
    parent: Optional['Node'] = None
    left_child: Optional['Node'] = None
    right_child: Optional['Node'] = None


def parse_node(value, parent=None):
    if isinstance(value, int):
        return Node(value=value, parent=parent)
    else:
        left, right = value
        node = Node(parent=parent)
        node.left_child = parse_node(left, parent=node)
        node.right_child = parse_node(right, parent=node)
        return node


def dump_node(node):
    if node.value is not None:
        return node.value
    else:
        return [dump_node(node.left_child), dump_node(node.right_child)]


def add_nodes(a, b):
    node = Node(left_child=a, right_child=b)
    a.parent = b.parent = node
    return node


def find_leftmost_leaf(node):
    curr_node = node
    while curr_node.parent and curr_node is curr_node.parent.left_child:
        curr_node = curr_node.parent
    if curr_node.parent:
        curr_node = curr_node.parent.left_child
        while curr_node.right_child:
            curr_node = curr_node.right_child
        return curr_node
    return None


def find_rightmost_leaf(node):
    curr_node = node
    while curr_node.parent and curr_node is curr_node.parent.right_child:
        curr_node = curr_node.parent
    if curr_node.parent:
        curr_node = curr_node.parent.right_child
        while curr_node.left_child:
            curr_node = curr_node.left_child
        return curr_node
    return None


def explode(node):
    leftmost_leaf = find_leftmost_leaf(node)
    if leftmost_leaf:
        leftmost_leaf.value += node.left_child.value
    rightmost_leaf = find_rightmost_leaf(node)
    if rightmost_leaf:
        rightmost_leaf.value += node.right_child.value
    node.left_child = node.right_child = None
    node.value = 0


def split(node):
    node.left_child = Node(value=math.floor(node.value / 2), parent=node)
    node.right_child = Node(value=math.ceil(node.value / 2), parent=node)
    node.value = None


def reduce_by_explosion(node, depth=0):
    if depth == 4 and node.value is None:
        explode(node)
        return True
    elif node.value is None:
        exploded = reduce_by_explosion(node.left_child, depth=depth+1)
        exploded |= reduce_by_explosion(node.right_child, depth=depth+1)
        return exploded
    return False


def reduce_by_split(node):
    if node.value is not None and node.value >= 10:
        split(node)
        return True
    elif node.value is None:
        split_in_left = reduce_by_split(node.left_child)
        if split_in_left:
            return True
        else:
            return reduce_by_split(node.right_child)
    return False


def reduce_in_order(node):
    keep_going = True
    while keep_going:
        something_exploded = reduce_by_explosion(node)
        something_split = reduce_by_split(node)
        keep_going = something_exploded or something_split


def magnitude(node):
    if node.value is not None:
        return node.value
    else:
        return 3 * magnitude(node.left_child) + 2 * magnitude(node.right_child)


if __name__ == "__main__":
    with open("inputs/input18.txt", "r") as f:
        lines = [json.loads(line) for line in f.read().splitlines()]
    nodes = [parse_node(line) for line in lines]
    sum_node = nodes.pop(0)
    while nodes:
        next_node = nodes.pop(0)
        sum_node = add_nodes(sum_node, next_node)
        reduce_in_order(sum_node)

    answer_a = magnitude(sum_node)
    print(f"Part A: {answer_a}")

    max_magnitude = 0
    for line_a, line_b in permutations(lines, 2):
        sum_a_b = add_nodes(parse_node(line_a), parse_node(line_b))
        reduce_in_order(sum_a_b)
        mag_a_b = magnitude(sum_a_b)
        if mag_a_b > max_magnitude:
            max_magnitude = mag_a_b
    print(f"Part B: {max_magnitude}")
