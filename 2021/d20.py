#!/usr/bin/env python3
from collections import defaultdict


def get_pixel_code(image, p_x, p_y):
    code = []
    for y in range(p_y - 1, p_y + 2):
        for x in range(p_x - 1, p_x + 2):
            pixel_value = image[x, y]
            code.append(1 if pixel_value == "#" else 0)
    return int(''.join(map(str, code)), 2)


def extend_image(image, algorithm):
    current_background = image.default_factory()
    new_background = algorithm[0] if current_background == "." else algorithm[511]
    new_image = defaultdict(lambda: new_background)
    size_x = max(x for x, y in image) + 3
    size_y = max(y for x, y in image) + 3

    for x in range(size_x):
        for y in range(size_y):
            pixel_code = get_pixel_code(image, x - 1, y - 1)
            new_image[x, y] = algorithm[pixel_code]
    return new_image


def parse_image(lines):
    image = defaultdict(lambda: ".")
    for y, line in enumerate(lines):
        for x, pixel in enumerate(line):
            image[x, y] = pixel
    return image


if __name__ == "__main__":
    with open("inputs/input20.txt", "r") as f:
        algorithm = f.readline()
        f.readline()
        image = parse_image(f.read().splitlines())

    for _ in range(2):
        image = extend_image(image, algorithm)
    answer_a = sum(p == "#" for p in image.values())
    print(f"Answer A: {answer_a}")

    for _ in range(48):
        image = extend_image(image, algorithm)
    answer_b = sum(p == "#" for p in image.values())
    print(f"Answer B: {answer_b}")
