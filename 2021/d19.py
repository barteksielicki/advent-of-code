#!/usr/bin/env python3
from collections import deque
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


class Scanner:
    def __init__(self, relative_beacon_positions):
        self.relative_beacons = relative_beacon_positions
        self.rotated_beacons = [
            [np.dot(rotation, beacon) for beacon in relative_beacon_positions]
            for rotation_idx, rotation in enumerate(POSSIBLE_ROTATIONS)
        ]
        self.beacon_characteristic = [
            [
                {tuple(beacon_a - beacon_b) for beacon_b in rotated_beacons}
                for beacon_a in rotated_beacons
            ]
            for rotated_beacons in self.rotated_beacons
        ]
        self.position = None
        self.correct_rotation = None

    @property
    def absolute_beacons(self):
        if self.position is None:
            raise Exception("Scanner not oriented!")
        return [self.position + beacon for beacon in self.rotated_beacons[self.correct_rotation]]

    def try_to_align_with(self, scanner):
        for rotation in range(len(POSSIBLE_ROTATIONS)):
            for beacon_a_idx, beacon_a_char in enumerate(self.beacon_characteristic[self.correct_rotation]):
                for beacon_b_idx, beacon_b_char in enumerate(scanner.beacon_characteristic[rotation]):
                    if len(beacon_a_char & beacon_b_char) >= 12:
                        scanner_position = (
                                self.position
                                + self.rotated_beacons[self.correct_rotation][beacon_a_idx]
                                - scanner.rotated_beacons[rotation][beacon_b_idx]
                        )
                        return rotation, scanner_position
        return None, None

    def manhattan_distance(self, scanner):
        return sum(map(abs, self.position - scanner.position))


def parse_scanners(lines):
    scanners = []
    beacons = None
    for line in lines:
        if not line:
            continue
        elif line.startswith("---"):
            if beacons:
                scanners.append(Scanner(beacons))
            beacons = []
        else:
            beacons.append(np.array([int(n) for n in line.split(",")]))
    scanners.append(Scanner(beacons))
    return scanners


if __name__ == "__main__":
    with open("inputs/input19.txt", "r") as f:
        lines = f.read().splitlines()
    scanners = parse_scanners(lines)

    scanners[0].position = np.array([0, 0, 0])
    scanners[0].correct_rotation = 0
    oriented_beacons = set(tuple(beacon) for beacon in scanners[0].absolute_beacons)
    queue = deque([scanners[0]])
    while len(queue):
        oriented_scanner = queue.popleft()
        for scanner in filter(lambda s: s.position is None, scanners):
            correct_rotation, scanner_position = oriented_scanner.try_to_align_with(scanner)
            if scanner_position is not None:
                scanner.correct_rotation = correct_rotation
                scanner.position = scanner_position
                oriented_beacons.update([tuple(beacon) for beacon in scanner.absolute_beacons])
                queue.append(scanner)

    print(f"Answer A: {len(oriented_beacons)}")
    max_distance = max(scanner_a.manhattan_distance(scanner_b) for scanner_a, scanner_b in combinations(scanners, 2))
    print(f"Answer B: {max_distance}")
