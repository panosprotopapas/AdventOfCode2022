import ast
from time import time


class Packet:
    def __init__(self, input_list):
        self.master_list = input_list
        self.flat_list = list()
        self.index = -1
        self.flatten_list([self.master_list])

    def flatten_list(self, input_list):
        length = len(input_list)
        index = 0
        for _ in range(length):
            item = input_list[index]
            is_list = True if type(item) is list else False
            previous_item = input_list[index - 1] if index > 0 else None
            next_item = input_list[index + 1] if index + 1 < length else None
            self.flat_list.append(
                {
                    "item": item,
                    "is_list": is_list,
                    "previous": previous_item,
                    "next": next_item,
                }
            )
            if is_list:
                self.flatten_list(input_list=item)
            index += 1


def is_ordered(packet_pair):
    l_packet = Packet(packet_pair[0])
    r_packet = Packet(packet_pair[1])
    l_was_integer = False
    r_was_integer = False

    l, r = 0, 0
    while l < len(l_packet.flat_list):
        l_item = l_packet.flat_list[l]
        try:
            r_item = r_packet.flat_list[r]
        except IndexError:
            return False
        l += 1
        r += 1

        # Both values are integers
        if not l_item["is_list"] and not r_item["is_list"]:
            if l_item["item"] < r_item["item"]:
                return True
            elif l_item["item"] > r_item["item"]:
                return False
            elif l_item["item"] == r_item["item"]:

                # Previous comparison was list against number
                if r_was_integer:
                    return False
                elif l_was_integer:
                    return True

                # List ends for one of the two
                elif l_item["next"] is None and r_item["next"] is not None:
                    return True
                elif l_item["next"] is not None and r_item["next"] is None:
                    return False
            continue

        # Both values are lists
        elif l_item["is_list"] and r_item["is_list"]:
            if len(l_item["item"]) == 0 and len(r_item["item"]) > 0:
                return True
            elif len(l_item["item"]) > 0 and len(r_item["item"]) == 0:
                return False
            continue

        # One value is list
        elif l_item["is_list"] and not r_item["is_list"]:
            if len(l_item["item"]) == 0:
                return True
            r -= 1
            r_was_integer = True
            continue
        elif not l_item["is_list"] and r_item["is_list"]:
            if len(r_item["item"]) == 0:
                return False
            l -= 1
            l_was_integer = True
            continue
    if len(l_packet.flat_list) == 0:
        return True


all_packets = [
    [ast.literal_eval(line.split("\n")[0]), ast.literal_eval(line.split("\n")[1])]
    for line in open("13/input.txt", "r").read().strip().split("\n\n")
]

# Part 1
result = sum([i + 1 for i, pair in enumerate(all_packets) if is_ordered(pair)])
print(f"Part 1: {result}")

# Part 2
left = [[2]]
right = [[6]]
a = time()
l_score = 1
r_score = 2
for packet in all_packets:
    for item in packet:
        if is_ordered([item, left]):
            l_score += 1
            r_score += 1
        elif is_ordered([item, right]):
            r_score += 1
print(f"Part 2: {l_score * r_score}")
