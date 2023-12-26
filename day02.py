with open('day02input.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# idsum = 0

# Determine which games would have been possible if the bag had been loaded with only
# 12 red cubes, 13 green cubes, and 14 blue cubes.
# What is the sum of the IDs of those games?

# part 2: find the sum of "powers" ie product of minimum r, g, b needed

powersum = 0

target = dict(red=12, green=13, blue=14)

# lines are like:
# Game 1: 7 green, 4 blue, 3 red; 4 blue, 10 red, 1 green; 1 blue, 9 red

for line in lines:
    idstr, drawstr = line.split(":")
    _id = int(idstr.split(" ")[1])
    draws = drawstr.split(";")
    max_draw = {}
    for draw in draws:
        items = draw.split(",")
        for item in items:
            num, color = item.strip().split(" ")
            num = int(num)
            if max_draw.get(color, 0) < num:
                max_draw[color] = num
    # for color, target_num in target.items():
    #     if max_draw[color] > target_num:
    #         print(f"Game {_id} is NOT possible because it has {max_draw[color]} {color} cubes")
    #         break
    # else:
    #     print(f"Game {_id} is possible!")
    #     idsum += _id
    power = max_draw["red"] * max_draw["green"] * max_draw["blue"]
    print(f"Game {_id}: {max_draw} -> power {power}")
    powersum += power

# print(idsum)
print(powersum)
