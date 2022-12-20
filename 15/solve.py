def interval(row_number, sensor_location, distance):
    if abs(row_number - sensor_location[1]) > distance:
        return None
    delta = abs(abs(row_number - sensor_location[1]) - distance)
    return [sensor_location[0] - delta, sensor_location[0] + delta]


def no_beacons_line(row_number, info, min_x):
    intervals = [
        interval(row_number, t[0], t[2])
        for t in info
        if interval(row_number, t[0], t[2]) is not None
    ]
    intervals = [[max(i[0], -min_x), min(i[1], 4000000 - min_x)] for i in intervals]
    master_intervals = [intervals[0]]
    for i in intervals[1:]:
        if i[0] > master_intervals[-1][1]:
            master_intervals.append(i)
        elif i[0] <= master_intervals[-1][0]:
            master_intervals[-1] = i
        elif i[1] > master_intervals[-1][1]:
            master_intervals[-1][1] = i[1]
    total = sum([i[1] - i[0] for i in master_intervals])
    return total, master_intervals


def no_beacons_line_part_1(row_number, info, min_x):
    intervals = [
        interval(row_number, t[0], t[2])
        for t in info
        if interval(row_number, t[0], t[2]) is not None
    ]
    intervals = [[i[0], i[1]] for i in intervals]
    master_intervals = [intervals[0]]
    for i in intervals[1:]:
        if i[0] > master_intervals[-1][1]:
            master_intervals.append(i)
        elif i[0] <= master_intervals[-1][0]:
            master_intervals[-1] = i
        elif i[1] > master_intervals[-1][1]:
            master_intervals[-1][1] = i[1]
    total = sum([i[1] - i[0] for i in master_intervals])
    return total


##########
# PART 1 #
##########
# Get sensor-beacon pairs
info = [
    [
        (int(i.split(", ")[0][2:]), int(i.split(", ")[1][2:]))
        for i in l.replace(" closest beacon is at ", "")
        .replace("Sensor at ", "")
        .split(":")
    ]
    for l in open("15/input.txt", encoding="utf-8").read().split("\n")
]

# Add distances to closest beacon
info = [[s, b, abs(s[0] - b[0]) + abs(s[1] - b[1])] for [s, b] in info]

# Find min/max x/y
min_x = min([triplet[0][0] - triplet[2] for triplet in info])
max_x = max([triplet[0][0] + triplet[2] for triplet in info])
min_y = min([triplet[0][1] - triplet[2] for triplet in info])
max_y = max([triplet[0][1] + triplet[2] for triplet in info])

# Normalize values
max_x = max_x - min_x
max_y = max_y - min_y
info = [
    [
        (triplet[0][0] - min_x, triplet[0][1] - min_y),
        (triplet[1][0] - min_x, triplet[1][1] - min_y),
        triplet[2],
    ]
    for triplet in info
]

# Sort triplets by sorting sensors from left to right
info.sort(key=lambda x: x[0][0])

# Part 1
print(f"Part 1: {no_beacons_line_part_1(2000000 - min_y, info, min_x)}")


# Part 2
for i in range(4000000):
    res, intervals = no_beacons_line(i - min_y, info, min_x)
    if res < 4000000:
        print(f"Part 2: {4000000 * (intervals[1][1] - intervals[0][1] - + min_x) + i}")
