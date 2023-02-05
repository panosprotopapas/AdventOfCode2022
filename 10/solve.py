class Solution:
    def __init__(self, commands):
        self.commands = commands
        self.signal_strength = list()
        self.x_vals = []
        self.picture = str()
        self.x = 1
        self.part_1()
        self.part_2()

    def part_1(self):
        i = 0
        for command in self.commands:
            i += 1
            if command[:4] == "noop":
                self.signal_strength.append(i * self.x)
                self.x_vals.append(self.x)
            else:
                self.signal_strength.append(i * self.x)
                self.x_vals.append(self.x)
                i += 1
                self.signal_strength.append(i * self.x)
                self.x_vals.append(self.x)
                self.x += int(command[5:])

    def part_2(self):
        for i, x in enumerate(self.x_vals):
            if i % 40 in [x - 1, x + 1, x]:
                self.picture += "#"
            else:
                self.picture += "."


with open("10/input.txt", encoding="utf-8") as f:
    commands = [line.strip() for line in f.readlines()]
s = Solution(commands)

# Part 1 Answer
part_1 = sum([s.signal_strength[i] for i in range(19, 240, 40)])
print(f"Part 1: {part_1}")

# Part 2 Answer
print("\nPart 2:")
for i in range(0, 240, 40):
    print(s.picture[i : i + 40])
