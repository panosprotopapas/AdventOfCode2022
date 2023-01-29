with open("6/input.txt") as f:
    line = f.readline()

part_1_not_done = True
for i in range(len(line)):
    if len(set(line[i:i+4])) == 4:
        if part_1_not_done:
            print(f"Part 1 {i+4}")
            part_1_not_done = False
        if len(set(line[i:i+14])) == 14:
            print(f"Part 2: {i+14}")
            break