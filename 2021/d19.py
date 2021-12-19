#!/usr/bin/env python3
from itertools import combinations

import numpy as np


POSSIBLE_ROTATIONS = [
    # Taken from: http://www.euclideanspace.com/maths/algebra/matrix/transforms/examples/index.htm
    np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]),
    np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]]),
    np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]),
    np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]),
    np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]]),
    np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]]),
    np.array([[0, 0, -1], [1, 0, 0], [0, -1, 0]]),
    np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]]),
    np.array([[-1, 0, 0], [0, 0, -1], [0, -1, 0]]),
    np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]]),
    np.array([[-1, 0, 0], [0, 0, 1], [0, 1, 0]]),
    np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]]),
    np.array([[0, 0, 1], [-1, 0, 0], [0, -1, 0]]),
    np.array([[0, -1, 0], [-1, 0, 0], [0, 0, -1]]),
    np.array([[0, 0, -1], [-1, 0, 0], [0, 1, 0]]),
    np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]]),
    np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]]),
    np.array([[0, 0, 1], [0, -1, 0], [1, 0, 0]]),
    np.array([[0, -1, 0], [0, 0, -1], [1, 0, 0]]),
    np.array([[0, 0, -1], [0, -1, 0], [-1, 0, 0]]),
    np.array([[0, -1, 0], [0, 0, 1], [-1, 0, 0]]),
    np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]),
    np.array([[0, 1, 0], [0, 0, -1], [-1, 0, 0]])
]


def parse_scanners(lines):
    scanners = []
    curr_scanner = None
    for line in lines:
        if not line:
            continue
        elif line.startswith("---"):
            if curr_scanner:
                scanners.append(curr_scanner)
            curr_scanner = []
        else:
            curr_scanner.append(np.array([int(n) for n in line.split(",")]))
    scanners.append(curr_scanner)
    return scanners


if __name__ == "__main__":
    with open("inputs/input19.txt", "r") as f:
        lines = f.read().splitlines()
    scanners = parse_scanners(lines)
    rotated_scanners = {}
    beacon_relations = {}
    for scanner_idx, scanner in enumerate(scanners):
        for rotation_idx, rotation in enumerate(POSSIBLE_ROTATIONS):
            rotated_scanner = [np.dot(rotation, beacon) for beacon in scanner]
            rotated_scanners[(scanner_idx, rotation_idx)] = rotated_scanner
            beacon_relations[(scanner_idx, rotation_idx)] = [
                [beacon_a - beacon_b for beacon_b in rotated_scanner]
                for beacon_a in rotated_scanner
            ]
    oriented_scanners = [0]
    scanners_positions = {0: np.array([0, 0, 0])}
    not_oriented_scanners = [i for i in range(1, len(scanners))]
    oriented_beacons = set(tuple(beacon) for beacon in scanners[0])
    checked_pairs = set()
    while not_oriented_scanners:
        should_break = False
        for scanner_idx in not_oriented_scanners:
            for oriented_scanner_idx in oriented_scanners:
                pair = (scanner_idx, oriented_scanner_idx)
                if pair in checked_pairs:
                    continue
                else:
                    checked_pairs.add(pair)
                oriented_scanner = scanners[oriented_scanner_idx]
                for rotation_idx in range(len(POSSIBLE_ROTATIONS)):
                    oriented_beacon_relations = beacon_relations[(oriented_scanner_idx, 0)]
                    to_check_beacon_relations = beacon_relations[(scanner_idx, rotation_idx)]
                    for beacon_a_idx, beacon_a_relations in enumerate(oriented_beacon_relations):
                        for beacon_b_idx, beacon_b_relations in enumerate(to_check_beacon_relations):
                            if len(set(tuple(v) for v in beacon_a_relations) & set(tuple(v) for v in beacon_b_relations)) >= 12:
                                print(f"Found match: {scanner_idx} and {oriented_scanner_idx}")
                                scanner_position = scanners_positions[oriented_scanner_idx] + oriented_scanner[beacon_a_idx] - rotated_scanners[(scanner_idx, rotation_idx)][beacon_b_idx]
                                scanners_positions[scanner_idx] = scanner_position
                                oriented_scanners.append(scanner_idx)
                                scanners[scanner_idx] = rotated_scanners[(scanner_idx, rotation_idx)]
                                beacon_relations[(scanner_idx, 0)] = to_check_beacon_relations
                                for beacon in scanners[scanner_idx]:
                                    oriented_beacons.add(tuple(beacon + scanner_position))
                                should_break = True
                                break
                        if should_break:
                            break
                    if should_break:
                        break
                if should_break:
                    break
            if should_break:
                oriented_scanners.append(scanner_idx)
                not_oriented_scanners.remove(scanner_idx)
                break
    print(f"Answer A: {len(oriented_beacons)}")
    max_distance = 0
    for scanner_a_idx, scanner_b_idx in combinations(scanners_positions, 2):
        x, y, z = scanners_positions[scanner_a_idx] - scanners_positions[scanner_b_idx]
        distance = abs(x) + abs(y) + abs(z)
        max_distance = max(distance, max_distance)
    print(f"Answer B: {max_distance}")
