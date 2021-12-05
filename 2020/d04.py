#!/usr/bin/env python3
import re


def read_passports_batch(input_lines):
    passports = []
    current_passport = {}
    for line in input_lines:
        if not line:  # is blank
            passports.append(current_passport)
            current_passport = {}
            continue
        for k, v in (field.split(":") for field in line.split()):
            current_passport[k] = v
    passports.append(current_passport)
    return passports


def is_valid_in_part_a(passport):
    required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    return not required_fields - set(passport.keys())


def is_valid_in_part_b(passport):
    def byr_valid(value):
        return bool(re.match(r"\d{4}", value) and 1920 <= int(value) <= 2002)

    def iyr_valid(value):
        return bool(re.match(r"\d{4}$", value) and 2010 <= int(value) <= 2020)

    def eyr_valid(value):
        return bool(re.match(r"\d{4}$", value) and 2020 <= int(value) <= 2030)

    def hgt_valid(value):
        match = re.match(r"(\d+)(cm|in)$", value)
        if not match:
            return False
        number, unit = match.groups()
        return (150 <= int(number) <= 193 and unit == "cm") or (59 <= int(number) <= 76 and unit == "in")

    def hcl_valid(value):
        return bool(re.match(r"#[a-f\d]{6}$", value))

    def ecl_valid(value):
        return value in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}

    def pid_valid(value):
        return bool(re.match(r"\d{9}$", value))

    if not is_valid_in_part_a(passport):
        return False

    return all((
        byr_valid(passport["byr"]),
        iyr_valid(passport["iyr"]),
        eyr_valid(passport["eyr"]),
        hgt_valid(passport["hgt"]),
        hcl_valid(passport["hcl"]),
        ecl_valid(passport["ecl"]),
        pid_valid(passport["pid"])
    ))


if __name__ == "__main__":
    with open("inputs/input04.txt", "r") as f:
        lines = f.read().splitlines()
    passports = read_passports_batch(lines)

    valid_passports_a = sum(is_valid_in_part_a(p) for p in passports)
    print(f"Part A: {valid_passports_a}")

    valid_passports_b = sum(is_valid_in_part_b(p) for p in passports)
    print(f"Part B: {valid_passports_b}")
