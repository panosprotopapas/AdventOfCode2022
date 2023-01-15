from time import time
from copy import copy

with open("21/input.txt", encoding="utf-8") as f:
    monkeys = [l.strip().split(": ") for l in f.readlines()]

for i, m in enumerate(monkeys):
    if m[0] == "humn":
        my_index = i
    elif m[0] == "root":
        root_index = i


def root_val(i_shout):
    monkeys[my_index][1] = i_shout
    monkeys_2 = copy(monkeys)
    new_monkeys = list()
    while monkeys_2:
        for _ in range(len(monkeys_2)):
            m = monkeys_2.pop(0)
            try:
                exec(f"{m[0]} = {m[1]}")
            except:
                new_monkeys.append(m)
        monkeys_2, new_monkeys = new_monkeys, list()
    return int(locals()["root"])


start = time()
print(f"Part 1: {root_val(monkeys[my_index][1])} | Time taken: {time() - start}")

start = time()
root_split = monkeys[root_index][1].split(" ")
monkeys[root_index][1] = f"{root_split[0]} - {root_split[2]}"

zero_me = 0
zero_root = root_val(zero_me)
current_me = 10**13
current_root = root_val(current_me)


zero_me = 0
while abs(current_root) > 150:
    if current_root * zero_root < 0:
        current_me = round(0.5 * (current_me + zero_me))
        current_root = root_val(current_me)
    else:
        zero_root = current_root
        current_me = round(2 * current_me - zero_me)
        zero_me = round(0.5 * (current_me + zero_me))
        current_root = root_val(current_me)

for i in [0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5, -6, 6, -7, 7, -8, 8, -9, 9]:
    if root_val(current_me + i):
        continue
    break

print(f"Part 2: {current_me+i} | Time taken: {time() - start}")
