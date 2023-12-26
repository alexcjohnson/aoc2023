import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

start_row, start_col = [(i, line.index("S")) for (i,line) in enumerate(lines) if "S" in line][0]
print("start position:", start_row, start_col)

steps = 0
if lines[start_row - 1][start_col] in "7|F":
    start_direction = (-1, 0)
elif lines[start_row + 1][start_col] in "J|L":
    start_direction = (1, 0)
else:
    start_direction = (0, 1)  # at this point we know we could go either left or right

direction = start_direction

links = {
    (-1, 0): {
        "7": (0, -1),
        "|": (-1, 0),
        "F": (0, 1)
    },
    (1, 0): {
        "J": (0, -1),
        "|": (1, 0),
        "L": (0, 1)
    },
    (0, -1): {
        "L": (-1, 0),
        "-": (0, -1),
        "F": (1, 0)
    },
    (0, 1): {
        "J": (-1, 0),
        "-": (0, 1),
        "7": (1, 0)
    }
}

part_of_loop = [[False for _ in line] for line in lines]

row, col = start_row, start_col
while steps < len(lines) * len(lines[0]):
    part_of_loop[row][col] = True
    row += direction[0]
    col += direction[1]
    steps += 1
    if lines[row][col] == "S":
        print(f"Looped! total steps: {steps}, farthest: {steps//2}")
        break
    direction = links[direction][lines[row][col]]

S_replaces = dict((v, k) for k, v in links[direction].items())[start_direction]

# now count loop crossings, following a path just ABOVE the centerline of each pipe
squares_inside = 0
for line, part_of_loop_line in zip(lines, part_of_loop):
    crossings = 0
    line_inside = ""
    for char, is_loop in zip(line, part_of_loop_line):
        if is_loop:
            if char in "J|L" or (char == "S" and S_replaces in "J|L"):
                crossings += 1
            line_inside += "."
        else:
            if crossings % 2:
                squares_inside += 1
                line_inside += "@"
            else:
                line_inside += " "
    print(line_inside)

print("squares inside: ", squares_inside)
