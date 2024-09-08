import operator
from dataclasses import dataclass
from functools import reduce
from math import ceil, isinf
from typing import Iterable

from utils import *


@dataclass
class Packet:
    version: int
    type: int
    total_length: int


@dataclass
class OperatorPacket(Packet):
    sub: list['Packet']


@dataclass
class LiteralPacket(Packet):
    value: int


def ceil_multiple(n: int, k: int):
    """Returns k*m such that (m-1)*k < n <= k*m"""
    return ceil(n / k) * k


def iter_groups(src: str, k: int):
    n = len(src) // k
    for i in range(0, n*k, k):
        yield src[i:i+k]


def parse_literal_packet_payload(payload: str) -> tuple[int, int]:
    """Parse literal packet without a-priori knowledge of its length"""
    n = ''
    for group in iter_groups(payload, 5):
        n += group[1:]
        if group[0] == '0':
            break

    # length related to useful bits
    payload_length = (len(n) // 4) * 5
    # # add the headers
    # total_pkt_length += 6
    # # due to hexadecimal representation, number of bits are a multiple of 4
    # total_pkt_length = ceil_multiple(total_pkt_length, 4)

    return int(n, 2), payload_length


def parse_packet(pkt: str):
    v, t, rest = pkt[:3], pkt[3:6], pkt[6:]
    v, t = int(v, 2), int(t, 2)

    if t == 4:
        value, payload_length = parse_literal_packet_payload(rest)
        return LiteralPacket(version=v, type=t, total_length=payload_length + 6, value=value)

    # otherwise, packet is of type operator
    length_type_id, payload = rest[0], rest[1:]

    if length_type_id == '0':
        length, payload = payload[:15], payload[15:]
        length = int(length, 2)
        payload = payload[:length]

        sub_packets = []
        while len(payload) > 0:
            pkt = parse_packet(payload)
            payload = payload[pkt.total_length:]
            sub_packets.append(pkt)

        # sum of sub packet total lengths may not be equal to length,
        # if that's the last packet (and hence padded with zeros due to hex repr)

        return OperatorPacket(version=v, type=t, total_length=6 + 1 + 15 + length, sub=sub_packets)

    length, payload = payload[:11], payload[11:]
    length = int(length, 2)
    sub_packets = []
    for _ in range(length):
        pkt = parse_packet(payload)
        payload = payload[pkt.total_length:]
        sub_packets.append(pkt)

    packets_length = sum(pkt.total_length for pkt in sub_packets)
    return OperatorPacket(version=v, type=t, total_length=6 + 1 + 11 + packets_length, sub=sub_packets)


# example = '00111000000000000110111101000101001010010001001000000000'
# pkt = parse_packet(example)
# assert pkt.version == 1 and pkt.type == 6
# assert len(pkt.sub) == 2
# assert pkt.sub[0].value == 10
# assert pkt.sub[1].value == 20


# example = '11101110000000001101010000001100100000100011000001100000'
# pkt = parse_packet(example)
# assert pkt.version == 7 and pkt.type == 3
# assert len(pkt.sub) == 3
# assert pkt.sub[0].value == 1 and pkt.sub[1].value == 2 and pkt.sub[2].value == 3

# example = parse_data('8A004A801A8002F478')
# pkt = parse_packet(example)
# assert pkt.version == 4 and len(pkt.sub) == 1
# pkt = pkt.sub[0]
# assert pkt.version == 1 and len(pkt.sub) == 1
# pkt = pkt.sub[0]
# assert pkt.version == 5 and len(pkt.sub) == 1
# pkt = pkt.sub[0]
# assert pkt.version == 6

def iter_sub_packets(pkt: Packet):
    q = [pkt]
    while len(q) > 0:
        pkt = q.pop()
        yield pkt

        if isinstance(pkt, OperatorPacket):
            q.extend(pkt.sub)


for data, expected_sum in [
    ('8A004A801A8002F478', 16),
    ('620080001611562C8802118E34', 12),
    ('C0015000016115A2E0802F182340', 23),
    ('A0016C880162017C3686B18A3D4780', 31)
]:
    pkt = parse_packet(parse_data(data))
    s = sum(pkt.version for pkt in iter_sub_packets(pkt))
    assert s == expected_sum


# ============== PART 1

data = parse_data(load_data())
pkt = parse_packet(data)
s = sum(pkt.version for pkt in iter_sub_packets(pkt))
print(s)


# ============== PART 2


OPERATORS = {
    0: sum,
    1: lambda numbers: reduce(lambda acc, n: acc * n, numbers, 1),
    2: min,
    3: max,
    5: lambda numbers: operator.gt(*numbers),
    6: lambda numbers: operator.lt(*numbers),
    7: lambda numbers: operator.eq(*numbers)
}


def compute_packet_value(pkt: Packet):
    if isinstance(pkt, LiteralPacket):
        return pkt.value

    return OPERATORS[pkt.type]([
        compute_packet_value(pkt) for pkt in pkt.sub
    ])


for data, expected_val in [
    ('C200B40A82', 3),
    ('04005AC33890', 54),
    ('9C0141080250320F1802104A08', 1),
    ('CE00C43D881120', 9),
    ('D8005AC2A8F0', 1),
    ('9C005AC2F8F0', 0)
]:
    pkt = parse_packet(parse_data(data))
    assert compute_packet_value(pkt) == expected_val


pkt = parse_packet(parse_data(load_data()))
print(compute_packet_value(pkt))
