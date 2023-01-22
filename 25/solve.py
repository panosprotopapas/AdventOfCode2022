from copy import copy

# Get map and create WindMap object
with open("25/input.txt", encoding="utf-8") as f:
    snafu_list = [[int(char.replace("-", "-1").replace("=", "-2")) for char in l.strip()] for l in f]

def snafu_to_dec(input):
    decimal = 0
    for power in range(0, len(input)):
        snafu = input.pop()
        decimal += snafu* (5**power)
    return decimal

def list_snafu_to_dec(input):
    return sum([snafu_to_dec(item) for item in input])

def dec_to_base_five(input):
    divider = 1
    while divider < input:
        divider *= 5
    result_str = ""
    while divider >=1:
        result_str += str(int(input // divider))
        input %= divider
        divider /= 5
    result_str = str(int(result_str))
    return [int(i) for i in result_str]

def base_five_to_snafu(input):
    output = copy(input)
    for i in range(len(input) - 1, -1, -1):
        if input[i] > 2:
            output[i-1] += 1
            input[i-1] += 1
            if input[i] == 3:
                output[i] = "="
            elif input[i] == 4:
                output[i] = "-"
            else:
                output[i] = "0"
        else:
            output[i] = str(input[i])
    return "".join(output)

def dec_to_snafu(input):
    return base_five_to_snafu(dec_to_base_five(input))

# print(list_snafu_to_dec(snafu_list))
print(f"Result: {dec_to_snafu(list_snafu_to_dec(snafu_list))}")
