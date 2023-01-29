# Get map and create WindMap object
with open("1/input.txt", encoding="utf-8") as f:
    numbers_str = [l.strip() for l in f]


numbers = list()
for n in numbers_str:
    if len(n):
        numbers.append(int(n))
    else:
        numbers.append(0)

totals, _sum = list(), 0
for n in numbers:
    if n:
        _sum += n
    else:
        totals.append(_sum)
        _sum = 0

totals.sort(reverse=True)

# Part 1
print(f"Part 1: {totals[0]}")
# Part 2
print(f"Part 2: {sum(totals[:3])}")
