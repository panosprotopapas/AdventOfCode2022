with open("4/input.txt") as f:
    sections = [
        sorted([list(map(int, item.split("-"))) for item in l.strip().split(",")])
        for l in f
    ]

print(f"Part 1: {sum([s[0][1] >= s[1][1] or s[0][0] == s[1][0] for s in sections])}")
print(f"Part 2: {sum([s[0][1] >= s[1][0] for s in sections])}")
