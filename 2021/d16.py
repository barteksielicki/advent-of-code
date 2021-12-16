#!/usr/bin/env python3
from itertools import islice
from dataclasses import dataclass
from typing import List, Optional


MIN_PACKET_LENGTH = 3 + 3 + 5


@dataclass
class Packet:
    version: int
    type_id: int
    literal_value: Optional[int] = None
    sub_packets: Optional[List['Packet']] = None


def hex_to_bits(message_hex):
    return ''.join(bin(int(char, base=16))[2:].zfill(4) for char in message_hex)


def read_raw_bits(n, message_iter):
    return ''.join(list(islice(message_iter, n)))


def read_bits(n, message_iter):
    return int(read_raw_bits(n, message_iter), 2)


def read_literal_value(message_iter):
    has_more_groups = read_bits(1, message_iter)
    number_in_binary = read_raw_bits(4, message_iter)
    while has_more_groups:
        has_more_groups = read_bits(1, message_iter)
        number_in_binary += read_raw_bits(4, message_iter)
    return int(number_in_binary, 2)


def parse_packet(message_iter):
    version = read_bits(3, message_iter)
    type_id = read_bits(3, message_iter)
    packet = Packet(version, type_id)
    if type_id == 4:
        packet.literal_value = read_literal_value(message_iter)
    else:
        length_type_id = read_bits(1, message_iter)
        if length_type_id == 0:
            sub_packets_bits_length = read_bits(15, message_iter)
            remaining_bits = read_raw_bits(sub_packets_bits_length, message_iter)
            packet.sub_packets = []
            while len(remaining_bits) >= MIN_PACKET_LENGTH:
                remaining_bits_iter = iter(remaining_bits)
                packet.sub_packets.append(parse_packet(remaining_bits_iter))
                remaining_bits = list(remaining_bits_iter)
        elif length_type_id == 1:
            sub_packets_count = read_bits(11, message_iter)
            packet.sub_packets = [parse_packet(message_iter) for _ in range(sub_packets_count)]
    return packet


def sum_version(packet):
    current_sum = packet.version
    if packet.sub_packets:
        for sub_packet in packet.sub_packets:
            current_sum += sum_version(sub_packet)
    return current_sum


def calculate_value(packet):
    if packet.type_id == 0:
        return sum(calculate_value(sub_packet) for sub_packet in packet.sub_packets)
    elif packet.type_id == 1:
        result = 1
        for sub_packet in packet.sub_packets:
            result *= calculate_value(sub_packet)
        return result
    elif packet.type_id == 2:
        return min(calculate_value(sub_packet) for sub_packet in packet.sub_packets)
    elif packet.type_id == 3:
        return max(calculate_value(sub_packet) for sub_packet in packet.sub_packets)
    elif packet.type_id == 4:
        return packet.literal_value
    elif packet.type_id == 5:
        return 1 if calculate_value(packet.sub_packets[0]) > calculate_value(packet.sub_packets[1]) else 0
    elif packet.type_id == 6:
        return 1 if calculate_value(packet.sub_packets[0]) < calculate_value(packet.sub_packets[1]) else 0
    elif packet.type_id == 7:
        return 1 if calculate_value(packet.sub_packets[0]) == calculate_value(packet.sub_packets[1]) else 0


if __name__ == "__main__":
    with open("inputs/input16.txt", "r") as f:
        message_hex = f.read()
    message_bits = hex_to_bits(message_hex)
    message_iter = iter(message_bits)
    root_packet = parse_packet(message_iter)

    answer_a = sum_version(root_packet)
    print(f"Part A: {answer_a}")

    answer_b = calculate_value(root_packet)
    print(f"Part B: {answer_b}")
