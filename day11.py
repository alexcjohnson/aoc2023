import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

empty_cols = [1 if all(line[i] != '#' for line in lines) else 0 for i in range(len(lines[0]))]
# print("".join("v" if e else " " for e in empty_cols))

empty_rows = [1 if "#" not in line else 0 for line in lines]
# print("\n".join(line + ("<" if e else "") for line, e in zip(lines, empty_rows)))

positions = []
for i, line in enumerate(lines):
    for j, char in enumerate(line):
        if char == "#":
            positions.append((j, i))

expansion = 1000000 - 1  # part 1 expansion = 1

total = 0
for i, (x1, y1) in enumerate(positions):
    for (x2, y2) in positions[i + 1:]:
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymin, ymax = min(y1, y2), max(y1, y2)
        total += xmax - xmin + ymax - ymin + expansion * (sum(empty_cols[xmin:xmax]) + sum(empty_rows[ymin:ymax]))

print(total)
