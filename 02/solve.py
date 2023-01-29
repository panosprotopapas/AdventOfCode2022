with open("2/input.txt", encoding="utf-8") as f:
    rounds = [l.strip().split(" ") for l in f]

part_1_dict = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
rounds = [(part_1_dict[r[0]], part_1_dict[r[1]]) for r in rounds]

def round_part_1(round):
    score = round[1]
    if round[0] == round[1]:
        score += 3
    elif round[0] == round[1] - 1:
        score += 6
    elif round[0] == round[1] + 2:
        score += 6
    return score

print(f"Part 1: {sum([round_part_1(r) for r in rounds])}")

def round_part_2(round):
    if round[1] == 1:
        score = round[0] - 1 if round[0] - 1 else 3
    elif round[1] == 2:
        score = round[0] + 3
    else:
        score = 6 + round[0] + 1 if round[0] + 1 < 4 else 7
    return score
    
print(f"Part 2: {sum([round_part_2(r) for r in rounds])}")
