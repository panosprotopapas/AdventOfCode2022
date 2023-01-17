import operator


class Elf:
    def __init__(self, x, y):
        self.loc = (x, y)
        self.gang = list()
        self.choice_index = 0
        self.order = {
            0: (self.can_move_up, self.move_up),
            1: (self.can_move_down, self.move_down),
            2: (self.can_move_left, self.move_left),
            3: (self.can_move_right, self.move_right),
        }
        self.proposal = None

    def propose(self):
        if self.is_alone():
            self.proposal = self.loc
        elif self.order[(self.choice_index % 4)][0]():
            self.proposal = self.order[(self.choice_index % 4)][1]()
        elif self.order[((self.choice_index + 1) % 4)][0]():
            self.proposal = self.order[((self.choice_index + 1) % 4)][1]()
        elif self.order[((self.choice_index + 2) % 4)][0]():
            self.proposal = self.order[((self.choice_index + 2) % 4)][1]()
        elif self.order[((self.choice_index + 3) % 4)][0]():
            self.proposal = self.order[((self.choice_index + 3) % 4)][1]()
        else:
            self.proposal = self.loc
        self.choice_index += 1
        return self.proposal

    def is_alone(self):
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x == y == 0:
                    continue
                if elves_dict.get(self.vector_addition(self.loc, (x, y))) is not None:
                    return False
        return True

    def can_move_up(self):
        for x in [-1, 0, 1]:
            if elves_dict.get(self.vector_addition(self.loc, (x, -1))) is not None:
                return False
        return True

    def move_up(self):
        return self.vector_addition(self.loc, (0, -1))

    def can_move_down(self):
        for x in [-1, 0, 1]:
            if elves_dict.get(self.vector_addition(self.loc, (x, 1))) is not None:
                return False
        return True

    def move_down(self):
        return self.vector_addition(self.loc, (0, 1))

    def can_move_left(self):
        for y in [-1, 0, 1]:
            if elves_dict.get(self.vector_addition(self.loc, (-1, y))) is not None:
                return False
        return True

    def move_left(self):
        return self.vector_addition(self.loc, (-1, 0))

    def can_move_right(self):
        for y in [-1, 0, 1]:
            if elves_dict.get(self.vector_addition(self.loc, (1, y))) is not None:
                return False
        return True

    def move_right(self):
        return self.vector_addition(self.loc, (1, 0))

    @staticmethod
    def vector_addition(a, b):
        return (a[0] + b[0], a[1] + b[1])

    def __repr__(self):
        return f"""{self.loc}"""


def round(elves):
    # First half
    propositions = dict()
    for elf in elves.values():
        p = elf.propose()
        if propositions.get(p):
            propositions[p] = False
        else:
            propositions[p] = True

    # Are we done?
    if all([elf.loc == elf.proposal for elf in elves.values()]):
        return True, elves

    # Second half
    for elf in list(elves.values()):
        if propositions[elf.proposal]:
            elves.pop(elf.loc)
            elf.loc = elf.proposal
            elf.proposal = None
            elves[elf.loc] = elf

    return False, elves


# Get map and find all elves
elves_dict = dict()
with open("23/input.txt", encoding="utf-8") as f:
    for y, row in enumerate(f.readlines()):
        for x, char in enumerate(row.strip()):
            if char == "#":
                elves_dict[(x, y)] = Elf(x, y)
for elf in elves_dict.values():
    elf.gang = elves_dict

### PART 1

# Get final round
for _ in range(10):
    final_round = round(elves_dict)[1]

# Find bounding box
min_x = min(elves_dict.keys(), key=lambda x: x[0])[0]
max_x = max(elves_dict.keys(), key=lambda x: x[0])[0]
min_y = min(elves_dict.keys(), key=lambda x: x[1])[1]
max_y = max(elves_dict.keys(), key=lambda x: x[1])[1]
bb_size = (max_x - min_x + 1) * (max_y - min_y + 1)
result_part_1 = bb_size - len(elves_dict)
print(f"Part 1: {result_part_1}")

### PART 2

# Get number of rounds
done = False
result_part_2 = 10   # start where we left off at part 1
while done is False:
    result_part_2 += 1
    done = round(elves_dict)[0]

print(f"Part 2: {result_part_2}")
