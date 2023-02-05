from math import sqrt
from pprint import pprint as print


class Solution:
    def __init__(self, head_moves, number_of_knots=2):
        self.moves = head_moves
        self.repeat = number_of_knots - 1
        self.current_trail = [(0, 0)]

    def get_first_trail(self):
        current_position = (0, 0)
        for move in self.moves:
            for _ in range(move[1]):
                if move[0] == "R":
                    current_position = (current_position[0], current_position[1] + 1)
                    self.current_trail.append(current_position)
                elif move[0] == "L":
                    current_position = (current_position[0], current_position[1] - 1)
                    self.current_trail.append(current_position)
                elif move[0] == "U":
                    current_position = (current_position[0] - 1, current_position[1])
                    self.current_trail.append(current_position)
                elif move[0] == "D":
                    current_position = (current_position[0] + 1, current_position[1])
                    self.current_trail.append(current_position)
                else:
                    raise BaseException(f"Wrong direction in moves provided: {move}")

    def get_final_trail(self):
        for _ in range(self.repeat):
            self.get_next_trail()

    def get_next_trail(self):
        current_position = (0, 0)
        next_trail = [(0, 0)]
        for trail_position in self.current_trail[1:]:
            if self.distance(current_position, trail_position) < 2:
                continue
            else:
                current_position = self.find_closest_adjacent_pt(
                    current_position, trail_position
                )
                next_trail.append(current_position)
        self.current_trail = next_trail

    def find_closest_adjacent_pt(self, current_position, h_pos):
        if h_pos == (-3, 4):
            pass
        starting_distance = self.distance(current_position, h_pos)
        result = current_position
        if self.distance((result[0] - 1, result[1]), h_pos) < starting_distance:
            result = (result[0] - 1, result[1])
        elif self.distance((result[0] + 1, result[1]), h_pos) < starting_distance:
            result = (result[0] + 1, result[1])
        new_distance = self.distance(result, h_pos)
        if new_distance > 1.1:
            if self.distance((result[0], result[1] - 1), h_pos) < new_distance:
                result = (result[0], result[1] - 1)
            elif self.distance((result[0], result[1] + 1), h_pos) < new_distance:
                result = (result[0], result[1] + 1)
        return result

    @staticmethod
    def distance(pos_1, pos_2):
        x_diff = pos_1[0] - pos_2[0]
        y_diff = pos_1[1] - pos_2[1]
        return sqrt(x_diff**2 + y_diff**2)


with open("09/input.txt", encoding="utf-8") as f:
    head_moves = [(l.strip().split(" ")[0], int(l.strip().split(" ")[1])) for l in f]

# Part 1 Answer
s = Solution(head_moves)
s.get_first_trail()
s.get_next_trail()
print(f"Part 1: {len(list(set(s.current_trail)))}")

# Part 2 Answer
s = Solution(head_moves, number_of_knots=10)
s.get_first_trail()
s.get_final_trail()
print(f"Part 2: {len(list(set(s.current_trail)))}")
