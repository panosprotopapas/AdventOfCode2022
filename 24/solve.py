class Wind:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def __repr__(self):
        return f"Location: {self.x, self.y}. Direction {self.direction}"


class WindsMap:
    def __init__(self, x, y, init_location):
        self.no_wind = Wind(0, 0, ".")
        self.states = {"0": list()}
        self.divisor = None
        self.size = (x, y)
        self.winds = dict()
        self.time = 0
        self.next_checklist = set()
        self.checklist = {init_location}

    def get_winds(self, time=None):
        time = time if time else self.time
        for y, line in enumerate(self.states[str(self.time)]):
            for x, char in enumerate(line):
                if char != ".":
                    self.winds[f"{x},{y}"] = [Wind(x, y, char)]

    def advance_winds(self):
        winds_dict = dict()
        for key in list(self.winds):
            winds = self.winds.pop(key)
            for wind in winds:
                if wind.direction == "^":
                    wind.y -= 1
                elif wind.direction == ">":
                    wind.x += 1
                elif wind.direction == "v":
                    wind.y += 1
                else:
                    wind.x -= 1
                if wind.x == -1:
                    wind.x = self.size[0] - 1
                elif wind.x == self.size[0]:
                    wind.x = 0
                elif wind.y == -1:
                    wind.y = self.size[1] - 1
                elif wind.y == self.size[1]:
                    wind.y = 0
                if winds_dict.get(f"{wind.x},{wind.y}"):
                    winds_dict[f"{wind.x},{wind.y}"].append(wind)
                else:
                    winds_dict[f"{wind.x},{wind.y}"] = [wind]
        self.winds = winds_dict

    def advance_state(self):
        self.advance_winds()

        new_state = list()
        for y in range(0, self.size[1]):
            line = str()
            for x in range(0, self.size[0]):
                winds = self.winds.get(f"{x},{y}")
                if winds is None:
                    line += "."
                elif len(winds) == 1:
                    line += winds[0].direction
                else:
                    line += str(len(winds))
            new_state.append(line)
        if new_state == self.states["0"]:
            return False
        else:
            self.time += 1
            self.states[f"{self.time}"] = new_state
            return True

    def find_states(self):
        self.get_winds()
        while self.advance_state():
            continue
        self.divisor = len(self.states)
        self.time = 0

    def next_empties(self):
        while len(self.checklist):
            location = self.checklist.pop()

            if location == (0, -1):
                self.next_checklist.add((0, -1))
                if self.is_empty((0, 0), self.time + 1):
                    self.next_checklist.add((0, 0))
            elif location == (winds_map.size[0] - 1, winds_map.size[1]):
                self.next_checklist.add((winds_map.size[0] - 1, winds_map.size[1]))
                if self.is_empty(
                    (winds_map.size[0] - 1, winds_map.size[1] - 1), self.time + 1
                ):
                    self.next_checklist.add(
                        (winds_map.size[0] - 1, winds_map.size[1] - 1)
                    )
            else:
                left_loc = (location[0] - 1, location[1]) if location[0] > 0 else None
                up_loc = (location[0], location[1] - 1) if location[1] > 0 else None
                right_loc = (
                    (location[0] + 1, location[1])
                    if location[0] + 1 < winds_map.size[0]
                    else None
                )
                down_loc = (
                    (location[0], location[1] + 1)
                    if location[1] + 1 < winds_map.size[1]
                    else None
                )

                for loc in [left_loc, up_loc, right_loc, down_loc, location]:
                    if loc and self.is_empty(loc, self.time + 1):
                        self.next_checklist.add(loc)

        self.checklist, self.next_checklist = self.next_checklist, set()
        self.time += 1

    def not_done(self, target):
        if target in self.checklist:
            return False
        else:
            return True

    def is_empty(self, location, time):
        x, y = location
        state = self.states[str(time % self.divisor)]
        return True if state[y][x] == "." else False


# Get map and create WindMap object
with open("24/input.txt", encoding="utf-8") as f:
    lines = list(f.readlines())
    winds_map = WindsMap(x=len(lines[0]) - 3, y=len(lines) - 2, init_location=(0, -1))
    for row in lines[1:-1]:
        winds_map.states["0"].append(row[1:-2])

# Part 1
winds_map.find_states()
while winds_map.not_done(target=(winds_map.size[0] - 1, winds_map.size[1] - 1)):
    winds_map.next_empties()
winds_map.time += 1
print(f"Part 1: {winds_map.time}")

# Part 2
winds_map.checklist = {(winds_map.size[0] - 1, winds_map.size[1])}
winds_map.next_checklist = set()
while winds_map.not_done(target=(0, 0)):
    winds_map.next_empties()
winds_map.time += 1
winds_map.checklist = {(0, -1)}
while winds_map.not_done(target=(winds_map.size[0] - 1, winds_map.size[1] - 1)):
    winds_map.next_empties()
print(f"Part 2: {winds_map.time + 1}")
