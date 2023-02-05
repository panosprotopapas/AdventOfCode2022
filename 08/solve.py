import numpy

with open("08/input.txt", encoding="utf-8") as f:
    trees = numpy.array([list(map(int, list(line.strip()))) for line in f.readlines()])

# First Part
part_1 = 4 * 99 - 4
for i in range(1, 98):
    for j in range(1, 98):
        if any(
            [
                True if trees[i][j] > max(trees[i, j + 1 :]) else False,
                True if trees[i][j] > max(trees[i, :j]) else False,
                True if trees[i][j] > max(trees[:i, j]) else False,
                True if trees[i][j] > max(trees[i + 1 :, j]) else False,
            ]
        ):
            part_1 += 1
print(f"Part 1: {part_1}")

# Second Part
def first_right(i, j):
    res = numpy.where(trees[i, j + 1 :] >= trees[i, j])[0]
    return res[0] + 1 if len(res) else len(trees[i, j + 1 :])


def first_left(i, j):
    res = numpy.where(trees[i, :j] >= trees[i, j])[0]
    return j - res[-1] if len(res) else len(trees[i, :j])


def first_up(i, j):
    res = numpy.where(trees[:i, j] >= trees[i, j])[0]
    return i - res[-1] if len(res) else len(trees[:i, j])


def first_down(i, j):
    res = numpy.where(trees[i + 1 :, j] >= trees[i, j])[0]
    return res[0] + 1 if len(res) else len(trees[i + 1 :, j])


part_2 = 0
for i in range(1, 98):
    for j in range(1, 98):
        part_2 = max(
            part_2,
            first_right(i, j) * first_left(i, j) * first_up(i, j) * first_down(i, j),
        )

print(f"Part 2: {part_2}")
