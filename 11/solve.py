from collections import deque
from copy import deepcopy
from math import prod


class Monkey:
    def __init__(self, items, operation, divisor, test):
        self.items = items
        self.operation = operation
        self.divisor = divisor
        self.test = test
        self.number_of_inspects = 0
        self.true = None
        self.false = None
        self.inspections = 0
        self.lcm = None

    def operate(self, old):
        return eval(self.operation)

    def assign_monkeys(self, monkeys):
        self.true = monkeys[self.test[True]]
        self.false = monkeys[self.test[False]]

    def assign_lcm(self, lcm):
        self.lcm = lcm

    def add_item(self, item):
        self.items.append(item)

    def inspect(self, part_1):
        item = self.items.popleft()
        item = self.operate(item)
        item = item % self.lcm
        if part_1:
            item = item // 3
        if item % self.divisor:
            self.false.add_item(item)
        else:
            self.true.add_item(item)


with open("11/input.txt", encoding="utf-8") as f:
    monkeys = dict()
    divisors = list()
    for l in f:
        if l.strip()[:6] == "Monkey":
            monkeys[int(l.strip().split(" ")[1][:-1])] = Monkey(
                items=deque(map(int, f.readline().strip().split(": ")[1].split(", "))),
                operation=f.readline().strip().split("= ")[1],
                divisor=int(f.readline().strip().split(" ")[-1]),
                test={
                    True: int(f.readline().strip().split(" ")[-1]),
                    False: int(f.readline().strip().split(" ")[-1]),
                },
            )
    for m in monkeys.values():
        m.assign_monkeys(monkeys)
        divisors.append(m.divisor)
    for m in monkeys.values():
        m.assign_lcm(prod(divisors))


def monkey_business(monkeys, rounds, part_1):
    for _ in range(
        rounds,
    ):
        for m_index in range(len(monkeys)):
            m = monkeys[m_index]
            m.inspections += len(m.items)
            for _ in range(len(m.items)):
                m.inspect(part_1=part_1)
    monkeys = sorted(monkeys.values(), key=lambda x: x.inspections, reverse=True)
    return monkeys[0].inspections * monkeys[1].inspections


print(
    f"Part 1: {monkey_business(monkeys= deepcopy(monkeys), rounds = 20, part_1 = True)}"
)
print(
    f"Part 1: {monkey_business(monkeys= deepcopy(monkeys), rounds = 10000, part_1 = False)}"
)
