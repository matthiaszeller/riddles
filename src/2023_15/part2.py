

from utils import *


def parse_step(step: str):
    if '=' in step:
        label, n = step.split('=')
        n = int(n)
        operation = '='
    else:
        label, n = step.strip('-'), -1
        operation = '-'

    return label, operation, n


steps = parse_data(load_data())
boxes = [
    {} for _ in range(256)
]
for step in steps:
    label, operation, n = parse_step(step)
    i = hash_algo(label)
    if operation == '-':
        if label in boxes[i]:
            del boxes[i][label]
    else:
        boxes[i][label] = n


P = 0
for i, box in enumerate(boxes, 1):
    for slot, fl in enumerate(box.values(), 1):
        P += i * slot * fl
