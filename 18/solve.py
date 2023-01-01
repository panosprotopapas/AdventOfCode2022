import numpy

with open("18/input.txt", encoding="utf-8") as f:
    coords = [
        tuple([int(i) for i in line.strip().split(",")]) for line in f.readlines()
    ]
min_x, max_x = min(coords, key=lambda i: i[0])[0], max(coords, key=lambda i: i[0])[0]
min_y, max_y = min(coords, key=lambda i: i[1])[1], max(coords, key=lambda i: i[1])[1]
min_z, max_z = min(coords, key=lambda i: i[2])[2], max(coords, key=lambda i: i[2])[2]
normalized_coords = [
    (c[0] - min_x + 1, c[1] - min_y + 1, c[2] - min_z + 1) for c in coords
]

np3d = numpy.zeros(shape=(max_x - min_x + 3, max_y - min_y + 3, max_z - min_z + 3))
for c in normalized_coords:
    np3d[c[0], c[1], c[2]] = 1


def check_edges(_map, cell, check):
    res = 0
    res += 1 if _map[cell[0] - 1, cell[1], cell[2]] == check else 0
    res += 1 if _map[cell[0] + 1, cell[1], cell[2]] == check else 0
    res += 1 if _map[cell[0], cell[1] - 1, cell[2]] == check else 0
    res += 1 if _map[cell[0], cell[1] + 1, cell[2]] == check else 0
    res += 1 if _map[cell[0], cell[1], cell[2] - 1] == check else 0
    res += 1 if _map[cell[0], cell[1], cell[2] + 1] == check else 0
    return res


# Part 1
surface_area = 0
for c in normalized_coords:
    surface_area += check_edges(_map=np3d, cell=c, check=0)
print(f"Part 1: {int(surface_area)}")

# Part 2

# Make all borders be steam
np3d[0:, 0:, 0] = "5"
np3d[0:, 0:, -1] = "5"
np3d[0, 0:, 0:] = "5"
np3d[-1, 0:, 0:] = "5"
np3d[0:, 0, 0:] = "5"
np3d[0:, -1, 0:] = "5"

# Find coords with zero value
all_coords = list()
for x in range(0, max_x - min_x + 2):
    for y in range(0, max_y - min_y + 2):
        for z in range(0, max_z - min_z + 2):
            all_coords.append((x, y, z))
zero_coords = list(set(all_coords) - set(normalized_coords))


# Recursively change emptiness to steam if conditions met
while True:
    new_coords = list()
    for c in zero_coords:
        if check_edges(_map=np3d, cell=c, check=5):
            np3d[c[0], c[1], c[2]] = 5
        else:
            new_coords.append(c)
    if len(zero_coords) == len(new_coords):
        break
    zero_coords, new_coords = new_coords, list()


# Count surfaces with steam
surface_area = 0
for c in normalized_coords:
    surface_area += check_edges(_map=np3d, cell=c, check=5)
print(f"Part 2: {int(surface_area)}")
