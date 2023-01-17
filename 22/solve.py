from re import findall


class Tile:
    def __init__(
        self,
        x=None,
        y=None,
        wall=False,
        up=None,
        down=None,
        left=None,
        right=None,
        position=None,
    ):
        self.x = x
        self.y = y
        self.wall = wall
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.position = position
        self.side = None
        self.cube_po = None


# Get instuctions and raw map
map = list()
instructions = list()
with open("22/input.txt", encoding="utf-8") as f:
    for l in f.readlines():
        line = l.rstrip()
        if line:
            if line[0].isalnum():
                line = "R" + line
                instructions += findall(r"\w\d+", line)
            else:
                map.append(line)

# Create a dictionary with all tiles
map_of_tiles = dict()
max_x, max_y = 1, 1
for y, row in enumerate(map):
    y += 1
    max_y = max(max_y, y)
    for x, character in enumerate(row):
        x += 1
        max_x = max(max_x, x)
        if character == ".":
            map_of_tiles[(x, y)] = Tile(x=x, y=y)
        elif character == "#":
            map_of_tiles[(x, y)] = Tile(x=x, y=y, wall=True)

# Fill in left and right for all tiles
for x in range(1, max_x + 1):
    ys = [
        map_of_tiles.get((x, y))
        for y in range(1, max_y + 1)
        if map_of_tiles.get((x, y))
    ]
    for i, tile in enumerate(ys):
        if i == 0:
            tile.up = ys[-1]
            tile.down = ys[i + 1]
        elif i == len(ys) - 1:
            tile.up = ys[i - 1]
            tile.down = ys[0]
        else:
            tile.up = ys[i - 1]
            tile.down = ys[i + 1]

# Fill in up and down for all tiles
for y in range(1, max_y + 1):
    xs = [
        map_of_tiles.get((x, y))
        for x in range(1, max_x + 1)
        if map_of_tiles.get((x, y))
    ]
    for i, tile in enumerate(xs):
        if i == 0:
            tile.left = xs[-1]
            tile.right = xs[i + 1]
        elif i == len(xs) - 1:
            tile.left = xs[i - 1]
            tile.right = xs[0]
        else:
            tile.left = xs[i - 1]
            tile.right = xs[i + 1]

### Part 1
on_tile = min(
    [map_of_tiles.get((x, 1)) for x in range(1, max_x + 1) if map_of_tiles.get((x, 1))],
    key=lambda i: i.x,
)
while on_tile.wall:
    on_tile = on_tile.right

facing = 3
for instruction in instructions:
    movement = int(instruction[1:])

    if instruction[0] == "R":
        facing = (facing + 1) % 4
    else:
        facing = (facing - 1) % 4

    while movement:
        movement -= 1
        if facing == 0:
            if on_tile.right.wall:
                break
            on_tile = on_tile.right
        elif facing == 1:
            if on_tile.down.wall:
                break
            on_tile = on_tile.down
        elif facing == 2:
            if on_tile.left.wall:
                break
            on_tile = on_tile.left
        elif facing == 3:
            if on_tile.up.wall:
                break
            on_tile = on_tile.up

part_1 = 1000 * (on_tile.y) + 4 * (on_tile.x) + facing
print(f"Part 1: {part_1}")

### Part 2

# Below solution only applies to some examples. Modify accordingly.
# Example type:
#          SIDE 1 - SIDE 2
#          SIDE 3
# SIDE 4 - SIDE 5
# SIDE 6

## Add tiles to their corresponding side

cube_map = dict()

# Side 1
for i, x in zip(range(1, 51), range(51, 101)):
    for j, y in zip(range(1, 51), range(1, 51)):
        tile = map_of_tiles.pop((x, y))
        tile.side = 1
        tile.cube_pos = (1, i, j)
        cube_map[(1, i, j)] = tile

# Side 2
for i, x in zip(range(1, 51), range(101, 151)):
    for j, y in zip(range(1, 51), range(1, 51)):
        tile = map_of_tiles.pop((x, y))
        tile.side = 2
        tile.cube_pos = (2, i, j)
        cube_map[(2, i, j)] = tile

# Side 3
for i, x in zip(range(1, 51), range(51, 101)):
    for j, y in zip(range(1, 51), range(51, 101)):
        tile = map_of_tiles.pop((x, y))
        tile.side = 3
        tile.cube_pos = (3, i, j)
        cube_map[(3, i, j)] = tile

# Side 4
for i, x in zip(range(1, 51), range(1, 51)):
    for j, y in zip(range(1, 51), range(101, 151)):
        tile = map_of_tiles.pop((x, y))
        tile.side = 4
        tile.cube_pos = (4, i, j)
        cube_map[(4, i, j)] = tile

# Side 5
for i, x in zip(range(1, 51), range(51, 101)):
    for j, y in zip(range(1, 51), range(101, 151)):
        tile = map_of_tiles.pop((x, y))
        tile.side = 5
        tile.cube_pos = (5, i, j)
        cube_map[(5, i, j)] = tile

# Side 6
for i, x in zip(range(1, 51), range(1, 51)):
    for j, y in zip(range(1, 51), range(151, 201)):
        tile = map_of_tiles.pop((x, y))
        tile.side = 6
        tile.cube_pos = (6, i, j)
        cube_map[(6, i, j)] = tile

## Connect sides that are not already connected

# Side 2's right is side's 5 right (upside down)
for y in range(1, 51):
    tile_2 = cube_map[(2, 50, y)]
    tile_5 = cube_map[(5, 50, 51 - y)]
    tile_2.right = tile_5
    tile_5.right = tile_2

# Side 4's left is side's 1 left (upside down)
for y in range(1, 51):
    tile_1 = cube_map[(1, 1, y)]
    tile_4 = cube_map[(4, 1, 51 - y)]
    tile_1.left = tile_4
    tile_4.left = tile_1

# Side 3's left is side's 4 up
for y in range(1, 51):
    tile_3 = cube_map[(3, 1, y)]
    tile_4 = cube_map[(4, y, 1)]
    tile_3.left = tile_4
    tile_4.up = tile_3

# Side 3's left is side's 4 up
for y in range(1, 51):
    tile_3 = cube_map[(3, 1, y)]
    tile_4 = cube_map[(4, y, 1)]
    tile_3.left = tile_4
    tile_4.up = tile_3

# Side 2's up is side 6's down
for y in range(1, 51):
    tile_2 = cube_map[(2, y, 1)]
    tile_6 = cube_map[(6, y, 50)]
    tile_2.up = tile_6
    tile_6.down = tile_2

# Side 2's down is side 3's right
for y in range(1, 51):
    tile_2 = cube_map[(2, y, 50)]
    tile_3 = cube_map[(3, 50, y)]
    tile_2.down = tile_3
    tile_3.right = tile_2

# Side 6's left is side 1's up
for y in range(1, 51):
    tile_1 = cube_map[(1, y, 1)]
    tile_6 = cube_map[(6, 1, y)]
    tile_1.up = tile_6
    tile_6.left = tile_1

# Side 6's right is side 5's down
for y in range(1, 51):
    tile_5 = cube_map[(5, y, 50)]
    tile_6 = cube_map[(6, 50, y)]
    tile_5.down = tile_6
    tile_6.right = tile_5

# Fix direction when needed during traveling from one side of the cube to the other
fix_dir = dict()
fix_dir[(2, 5)] = fix_dir[(5, 2)] = fix_dir[(1, 4)] = fix_dir[(4, 1)] = 2
fix_dir[(6, 1)] = fix_dir[(3, 2)] = fix_dir[(3, 4)] = fix_dir[(6, 5)] = -1
fix_dir[(1, 6)] = fix_dir[(2, 3)] = fix_dir[(4, 3)] = fix_dir[(5, 6)] = 1

# Start conditions
on_tile = cube_map[(1, 1, 1)]  # In my sample, first choice is not wall
on_side = 1
facing = 3

# Solve
for instruction in instructions:
    movement = int(instruction[1:])

    if instruction[0] == "R":
        facing = (facing + 1) % 4
    else:
        facing = (facing - 1) % 4

    while movement:
        movement -= 1
        if facing == 0:
            if on_tile.right.wall:
                break
            on_tile = on_tile.right
        elif facing == 1:
            if on_tile.down.wall:
                break
            on_tile = on_tile.down
        elif facing == 2:
            if on_tile.left.wall:
                break
            on_tile = on_tile.left
        elif facing == 3:
            if on_tile.up.wall:
                break
            on_tile = on_tile.up
        if on_side != on_tile.side:
            facing = (facing + fix_dir.get((on_side, on_tile.side), 0)) % 4
            on_side = on_tile.side

print(f"Part 2: {1000 * (on_tile.y) + 4 * (on_tile.x) + facing}")
