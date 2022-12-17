import numpy

##########
# PART 1 #
##########

# Get rock paths
rock_paths = [
    [(int(i.split(",")[0]), int(i.split(",")[1])) for i in l.split(" -> ")]
    for l in open("14/input.txt", encoding="utf-8").read().split("\n")
]

# Get edges of bounding box
max_x = max([max([coord[0] for coord in path]) for path in rock_paths])
min_x = min([min([coord[0] for coord in path]) for path in rock_paths])
max_y = max([max([coord[1] for coord in path]) for path in rock_paths])


# Normalize
max_x = max_x - min_x
sand_flow_x = 500 - min_x
rock_paths = [[(coord[0] - min_x, coord[1]) for coord in path] for path in rock_paths]

# Create diagram and fill with rocks and sand source
diagram = numpy.chararray((max_y + 1, max_x + 1), unicode=True)
diagram[:] = "."
diagram[0, sand_flow_x] = "+"
for path in rock_paths:
    for i in range(len(path) - 1):
        top_left = (
            min([i[0] for i in [path[i], path[i + 1]]]),
            min([i[1] for i in [path[i], path[i + 1]]]),
        )
        bottom_right = (
            max([i[0] for i in [path[i], path[i + 1]]]),
            max([i[1] for i in [path[i], path[i + 1]]]),
        )
        diagram[
            top_left[1] : bottom_right[1] + 1, top_left[0] : bottom_right[0] + 1
        ] = "#"

# Fill with sand
try:
    while True:
        pos = (0, sand_flow_x)
        while True:
            if diagram[pos[0] + 1, pos[1]] == ".":
                pos = (pos[0] + 1, pos[1])
                continue
            if diagram[pos[0] + 1, pos[1] - 1] == ".":
                pos = (pos[0] + 1, pos[1] - 1)
                continue
            if diagram[pos[0] + 1, pos[1] + 1] == ".":
                pos = (pos[0] + 1, pos[1] + 1)
                continue
            diagram[pos[0], pos[1]] = "O"
            break
except IndexError:
    print(f"""Part 1: {numpy.count_nonzero(diagram == "O")}""")
    numpy.savetxt("14/part_1_end.csv", diagram, delimiter=",", encoding="utf8", fmt="%s")

##########
# PART 2 #
##########

# Get rock paths
rock_paths = [
    [(int(i.split(",")[0]), int(i.split(",")[1])) for i in l.split(" -> ")]
    for l in open("14/input.txt", encoding="utf-8").read().split("\n")
]

# Get edges of bounding box
max_y = max([max([coord[1] for coord in path]) for path in rock_paths]) + 2
min_x = min([min([coord[0] for coord in path]) for path in rock_paths]) - max_y
max_x = max([max([coord[0] for coord in path]) for path in rock_paths]) + max_y

# Add floor
rock_paths.append([(min_x, max_y), (max_x, max_y)])

# Normalize
max_x = max_x - min_x
sand_flow_x = 500 - min_x
rock_paths = [[(coord[0] - min_x, coord[1]) for coord in path] for path in rock_paths]

# Create diagram and fill with rocks and sand source
diagram = numpy.chararray((max_y + 1, max_x + 1), unicode=True)
diagram[:] = "."
diagram[0, sand_flow_x] = "+"
for path in rock_paths:
    for i in range(len(path) - 1):
        top_left = (
            min([i[0] for i in [path[i], path[i + 1]]]),
            min([i[1] for i in [path[i], path[i + 1]]]),
        )
        bottom_right = (
            max([i[0] for i in [path[i], path[i + 1]]]),
            max([i[1] for i in [path[i], path[i + 1]]]),
        )
        diagram[
            top_left[1] : bottom_right[1] + 1, top_left[0] : bottom_right[0] + 1
        ] = "#"

# Fill with sand
while numpy.count_nonzero(diagram[1, sand_flow_x - 1: sand_flow_x + 2] == "."):
    pos = (0, sand_flow_x)
    while True:
        if diagram[pos[0] + 1, pos[1]] == ".":
            pos = (pos[0] + 1, pos[1])
            continue
        if diagram[pos[0] + 1, pos[1] - 1] == ".":
            pos = (pos[0] + 1, pos[1] - 1)
            continue
        if diagram[pos[0] + 1, pos[1] + 1] == ".":
            pos = (pos[0] + 1, pos[1] + 1)
            continue
        diagram[pos[0], pos[1]] = "O"
        break

print(f"""Part 2: {numpy.count_nonzero(diagram == "O") + 1}""")
numpy.savetxt("14/part_2_end.csv", diagram, delimiter=",", encoding="utf8", fmt="%s")