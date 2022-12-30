from abc import ABC, abstractclassmethod
from pprint import pprint as print

class State:
    def __init__(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            self.jet_pattern = f.read().strip()
        self.jet_index = 0
        self.cave = ["|.......|", "|.......|", "|.......|", "+-------+"]
        self.jet_length = len(self.jet_pattern)

    def __repr__(self):
        return f"{self.cave}"


class BaseRock(ABC):
    @abstractclassmethod
    def insert_shape(self):
        pass

    @abstractclassmethod
    def can_move_down(self):
        pass

    @abstractclassmethod
    def place(self):
        pass

    @abstractclassmethod
    def let_it_fall(self):
        pass

    def is_left_jet(self):
        # Is it left or right jet?
        left_jet = (
            True
            if self.state.jet_pattern[self.state.jet_index % self.state.jet_length]
            == "<"
            else False
        )
        self.state.jet_index += 1

        return left_jet

    def fix_map(self):
        while self.state.cave[3] == "|.......|":
            self.state.cave.pop(0)
        while self.state.cave[2] != "|.......|":
            self.state.cave.insert(0, "|.......|")

    def let_it_fall(self):
        self.insert_shape()
        while self.can_move_down():
            self.cave_index += 1
        self.place()
        self.fix_map()


class LineHorizontal(BaseRock):
    def __init__(self, state):
        self.state = state
        self.cave_index = 0
        self.left_edge = 3
        self.right_edge = 6
        self.let_it_fall()

    def insert_shape(self):
        self.state.cave.insert(0, "|.......|")

    def can_move_down(self):
        self.jet_move()
        # Can it move down?
        if (
            self.state.cave[self.cave_index + 1][self.left_edge : self.right_edge + 1]
            == "...."
        ):
            return True

    def jet_move(self):
        # Move according to jet
        left_jet = self.is_left_jet()
        if left_jet and self.state.cave[self.cave_index][self.left_edge - 1] == ".":
            self.left_edge -= 1
            self.right_edge -= 1
        elif (
            not left_jet
            and self.state.cave[self.cave_index][self.right_edge + 1] == "."
        ):
            self.left_edge += 1
            self.right_edge += 1

    def place(self):
        self.state.cave[self.cave_index] = (
            self.state.cave[self.cave_index][: self.left_edge]
            + "####"
            + self.state.cave[self.cave_index][self.right_edge + 1 :]
        )


class Cross(BaseRock):
    def __init__(self, state):
        self.state = state
        self.cave_index = 0
        self.centre = 4
        self.let_it_fall()

    def insert_shape(self):
        self.state.cave = ["|.......|", "|.......|", "|.......|"] + self.state.cave

    def can_move_down(self):
        self.jet_move()
        # Can it move down?
        if (
            self.state.cave[self.cave_index + 2][self.centre - 1] == "."
            and self.state.cave[self.cave_index + 2][self.centre + 1] == "."
            and self.state.cave[self.cave_index + 3][self.centre] == "."
        ):
            return True

    def jet_move(self):
        # Move according to jet
        left_jet = self.is_left_jet()
        if (
            left_jet
            and self.state.cave[self.cave_index][self.centre - 1] == "."
            and self.state.cave[self.cave_index + 1][self.centre - 2] == "."
            and self.state.cave[self.cave_index + 2][self.centre - 1] == "."
        ):
            self.centre -= 1
        elif (
            not left_jet
            and self.state.cave[self.cave_index][self.centre + 1] == "."
            and self.state.cave[self.cave_index + 1][self.centre + 2] == "."
            and self.state.cave[self.cave_index + 2][self.centre + 1] == "."
        ):
            self.centre += 1

    def place(self):
        self.state.cave[self.cave_index] = (
            self.state.cave[self.cave_index][: self.centre]
            + "#"
            + self.state.cave[self.cave_index][self.centre + 1 :]
        )
        self.state.cave[self.cave_index + 1] = (
            self.state.cave[self.cave_index + 1][: self.centre - 1]
            + "###"
            + self.state.cave[self.cave_index + 1][self.centre + 2 :]
        )
        self.state.cave[self.cave_index + 2] = (
            self.state.cave[self.cave_index + 2][: self.centre]
            + "#"
            + self.state.cave[self.cave_index + 2][self.centre + 1 :]
        )


class Corner(BaseRock):
    def __init__(self, state):
        self.state = state
        self.cave_index = 0
        self.top = 5
        self.let_it_fall()

    def insert_shape(self):
        self.state.cave = ["|.......|", "|.......|", "|.......|"] + self.state.cave

    def can_move_down(self):
        self.jet_move()
        # Can it move down?
        if self.state.cave[self.cave_index + 3][self.top - 2 : self.top + 1] == "...":
            return True

    def jet_move(self):
        # Move according to jet
        left_jet = self.is_left_jet()
        if (
            left_jet
            and self.state.cave[self.cave_index][self.top - 1] == "."
            and self.state.cave[self.cave_index + 1][self.top - 1] == "."
            and self.state.cave[self.cave_index + 2][self.top - 3] == "."
        ):
            self.top -= 1
        elif (
            not left_jet
            and self.state.cave[self.cave_index][self.top + 1] == "."
            and self.state.cave[self.cave_index + 1][self.top + 1] == "."
            and self.state.cave[self.cave_index + 2][self.top + 1] == "."
        ):
            self.top += 1

    def place(self):
        self.state.cave[self.cave_index] = (
            self.state.cave[self.cave_index][: self.top]
            + "#"
            + self.state.cave[self.cave_index][self.top + 1 :]
        )
        self.state.cave[self.cave_index + 1] = (
            self.state.cave[self.cave_index + 1][: self.top]
            + "#"
            + self.state.cave[self.cave_index + 1][self.top + 1 :]
        )
        self.state.cave[self.cave_index + 2] = (
            self.state.cave[self.cave_index + 2][: self.top - 2]
            + "###"
            + self.state.cave[self.cave_index + 2][self.top + 1 :]
        )


class LineVertical(BaseRock):
    def __init__(self, state):
        self.state = state
        self.cave_index = 0
        self.top = 3
        self.let_it_fall()

    def insert_shape(self):
        self.state.cave = [
            "|.......|",
            "|.......|",
            "|.......|",
            "|.......|",
        ] + self.state.cave

    def can_move_down(self):
        self.jet_move()
        # Can it move down?
        if self.state.cave[self.cave_index + 4][self.top] == ".":
            return True

    def jet_move(self):
        # Move according to jet
        left_jet = self.is_left_jet()
        if (
            left_jet
            and self.state.cave[self.cave_index][self.top - 1] == "."
            and self.state.cave[self.cave_index + 1][self.top - 1] == "."
            and self.state.cave[self.cave_index + 2][self.top - 1] == "."
            and self.state.cave[self.cave_index + 3][self.top - 1] == "."
        ):
            self.top -= 1
        elif (
            not left_jet
            and self.state.cave[self.cave_index][self.top + 1] == "."
            and self.state.cave[self.cave_index + 1][self.top + 1] == "."
            and self.state.cave[self.cave_index + 2][self.top + 1] == "."
            and self.state.cave[self.cave_index + 3][self.top + 1] == "."
        ):
            self.top += 1

    def place(self):
        self.state.cave[self.cave_index] = (
            self.state.cave[self.cave_index][: self.top]
            + "#"
            + self.state.cave[self.cave_index][self.top + 1 :]
        )
        self.state.cave[self.cave_index + 1] = (
            self.state.cave[self.cave_index + 1][: self.top]
            + "#"
            + self.state.cave[self.cave_index + 1][self.top + 1 :]
        )
        self.state.cave[self.cave_index + 2] = (
            self.state.cave[self.cave_index + 2][: self.top]
            + "#"
            + self.state.cave[self.cave_index + 2][self.top + 1 :]
        )
        self.state.cave[self.cave_index + 3] = (
            self.state.cave[self.cave_index + 3][: self.top]
            + "#"
            + self.state.cave[self.cave_index + 3][self.top + 1 :]
        )


class Square(BaseRock):
    def __init__(self, state):
        self.state = state
        self.cave_index = 0
        self.top_left = 3
        self.let_it_fall()

    def insert_shape(self):
        self.state.cave = [
            "|.......|",
            "|.......|",
        ] + self.state.cave

    def can_move_down(self):
        self.jet_move()
        # Can it move down?
        if (
            self.state.cave[self.cave_index + 2][self.top_left : self.top_left + 2]
            == ".."
        ):
            return True

    def jet_move(self):
        # Move according to jet
        left_jet = self.is_left_jet()
        if (
            left_jet
            and self.state.cave[self.cave_index][self.top_left - 1] == "."
            and self.state.cave[self.cave_index + 1][self.top_left - 1] == "."
        ):
            self.top_left -= 1
        elif (
            not left_jet
            and self.state.cave[self.cave_index][self.top_left + 2] == "."
            and self.state.cave[self.cave_index + 1][self.top_left + 2] == "."
        ):
            self.top_left += 1

    def place(self):
        self.state.cave[self.cave_index] = (
            self.state.cave[self.cave_index][: self.top_left]
            + "##"
            + self.state.cave[self.cave_index][self.top_left + 2 :]
        )
        self.state.cave[self.cave_index + 1] = (
            self.state.cave[self.cave_index + 1][: self.top_left]
            + "##"
            + self.state.cave[self.cave_index + 1][self.top_left + 2 :]
        )


def part_1(number_of_rocks):
    rock_index = 0
    sequence_of_rocks = [LineHorizontal, Cross, Corner, LineVertical, Square]
    state = State(filepath="17/input.txt")

    for i in range(number_of_rocks):
        rock_shape = sequence_of_rocks[rock_index % 5]
        rock = rock_shape(state)
        state = rock.state
        rock_index += 1
    return len(rock.state.cave) - 4


print(f"Part 1: {part_1(2022)}")

# For part 2, check after how many rocks a full line is filled (a disappearing line in Tetris)
# In my case this is after 1371 rocks. And then after 1745 more, and so on and so forth.First rock 
# after this 1372nd is a Cross which is a bummer since 1st rock is a Horizontal line and can't 
# directly use a repetition. However, I checked in my example, and the bottom line does not interfere
# with any other rocks apart from the very first one. So can actually use the repetition :D

# Every time the pattern repeats you get an extra part_1(3116) - part_1(1371) lines.
repeat_lines = part_1(3116) - part_1(1371)

# 1000000000000 rocks have number of repetitions and lines
repeated_times = 1000000000000 // (3116-1371)
repeated_height = repeated_times * repeat_lines

# To this need to add the first rock-line AND the height created by the remainder which starts with
# a Cross. Since Cross comes after Horizontal Line, can just find the height directly
remainder_rocks = 1000000000000 % (3116-1371)
remainder_height = part_1(remainder_rocks)

# Part 2 answer
print(f"Part 2: {repeated_height + remainder_height}")
