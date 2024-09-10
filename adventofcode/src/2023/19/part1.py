import re

from utils import *


def process_part(workflows, part: dict[str, int], start='in'):
    rules = workflows[start]
    for rule in rules:
        condition = re.search(r'(\w+)([<>])(\d+):(\w+)', rule)
        if condition is not None:
            attr, operator, num, decision = condition.groups()
            condition_bool = eval(f'{part[attr]} {operator} {num}')
            if condition_bool:
                if decision in {'A', 'R'}:
                    return decision
                return process_part(workflows, part, start=decision)

        else:
            if rule in {'A', 'R'}:
                return rule
            return process_part(workflows, part, start=rule)


def solve(workflows, parts):
    parts = [
        part for part in parts
        if process_part(workflows, part) == 'A'
    ]
    return sum(
        v
        for p in parts
        for v in p.values()
    )


workflows, parts = parse_data(load_data())
print(solve(workflows, parts))
