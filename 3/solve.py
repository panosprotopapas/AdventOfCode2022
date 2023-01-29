def score_func(c):
    if c.isupper():
        return ord(c) - 38
    return ord(c) - 96


# Part 1
with open("3/input.txt") as f:
    sacks = [
        [
            set(l.strip()[: int(len(l.strip()) / 2)]),
            set(l.strip()[int(len(l.strip()) / 2) :]),
        ]
        for l in f
    ]

common = [list(s[0].intersection(s[1]))[0] for s in sacks]
score = sum([score_func(c) for c in common])
print(f"Part 1: {score}")

# Part 2
with open("3/input.txt") as f:
    sacks = [l.strip() for l in f]

score = 0
for i in range(0, len(sacks), 3):
    c = list(
        set(sacks[i]).intersection(set(sacks[i + 1])).intersection(set(sacks[i + 2]))
    )[0]
    score += score_func(c)

print(f"Part 2: {score}")
