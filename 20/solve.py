from time import time

with open("20/input.txt", encoding="utf-8") as f:
    message_part_1 = [int(l.strip()) for l in f.readlines()]

with open("20/input.txt", encoding="utf-8") as f:
    message_part_2 = [(int(l.strip()) * 811589153) for l in f.readlines()]


class Coord:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Value: {self.value}\nLeft: {self.left.value}\nRight:{self.right.value}\n\n"


def decrypt(message, rounds):
    globe = [Coord(val) for val in message]
    globe_round = len(globe) - 1

    for i, coord in enumerate(globe):
        coord.left = globe[i - 1]
        if i == len(globe) - 1:
            coord.right = globe[0]
        else:
            coord.right = globe[i + 1]

    for _ in range(rounds):
        for coord in globe:

            # remove from initial location
            coord.left.right = coord.right
            coord.right.left = coord.left

            # find new location
            if coord.value >= 0:
                left_coord = coord.left
                for _ in range(coord.value % globe_round):
                    left_coord = left_coord.right
                right_coord = left_coord.right
            else:
                right_coord = coord.right
                for _ in range(-coord.value % globe_round):
                    right_coord = right_coord.left
                left_coord = right_coord.left

            # add to new location
            coord.left, coord.right = left_coord, right_coord
            left_coord.right, right_coord.left = coord, coord

    # Find zero coordinate
    for coord in globe:
        if coord.value == 0:
            break

    # Get result
    result = 0
    for i in range(3001):
        if i % 1000 == 0:
            result += coord.value
        coord = coord.right

    return result


print(f"Part 1: {decrypt(message=message_part_1, rounds=1)}")
print(f"Part 2: {decrypt(message=message_part_2, rounds=10)}")
