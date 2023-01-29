from pprint import pprint as print
import re
from copy import copy, deepcopy

with open("5/input.txt") as f:
    stacks_raw = [next(f).replace("\n", "") for _ in range(8)]
    next(f)
    next(f)
    orders = [list(map(int, re.findall(r"\d+", l))) for l in f.readlines()]

stacks = [list(), list(), list(), list(), list(), list(), list(), list(), list()]
for s in stacks_raw[::-1]:
    for i, j in zip(range(9), range(1, 35, 4)):
        if s[j] != " ":
            stacks[i].append(s[j])

stacks_part_1 = deepcopy(stacks)
for (a, b, c) in orders:
    for _ in range(a):
        stacks_part_1[c - 1].append(stacks_part_1[b - 1].pop())

for (a, b, c) in orders:
    stacks[c - 1].extend(stacks[b - 1][-a:])
    stacks[b - 1] = stacks[b - 1][:-a]

print(f"""Part 1: {"".join([s[-1] for s in stacks_part_1])}""")
print(f"""Part 2: {"".join([s[-1] for s in stacks])}""")
