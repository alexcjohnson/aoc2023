import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

maxrow = len(lines) - 1
maxcol = len(lines[0]) - 1


def oob(row, col):
    return row < 0 or row > maxrow or col < 0 or col > maxcol


def propagate(row, col, dr, dc, active):
    if oob(row, col) or (dr, dc) in active[row][col]:
        return []
    active[row][col].add((dr, dc))
    char = lines[row][col]
    if char == "." or (char == "-" and not dr) or (char == "|" and not dc):
        return [(row + dr, col + dc, dr, dc)]
    elif char in "/\\":
        newdr, newdc = (dc, dr) if char == "\\" else (-dc, -dr)
        return [(row + newdr, col + newdc, newdr, newdc)]
    else:  # flat side of splitter
        return [(row + dc, col + dr, dc, dr), (row - dc, col - dr, -dc, -dr)]


def find_total(row, col, dr, dc):
    active = [[set() for _ in line] for line in lines]
    beams = [(row, col, dr, dc)]
    while beams:
        new_beams = []
        for beam in beams:
            new_beams += propagate(*beam, active)
        beams = new_beams

    return sum(sum(1 if el else 0 for el in row) for row in active)


print(find_total(0, 0, 0, 1))  # part 1

max_total = 0

for r in range(len(lines)):
    from_left = find_total(r, 0, 0, 1)
    from_right = find_total(r, maxcol, 0, -1)
    max_total = max(max_total, from_left, from_right)

for c in range(len(lines[0])):
    from_top = find_total(0, c, 1, 0)
    from_bottom = find_total(maxrow, c, -1, -0)
    max_total = max(max_total, from_top, from_bottom)

print(max_total)  # part 2
