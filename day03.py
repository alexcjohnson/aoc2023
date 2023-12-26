import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

chars = [[c for c in l] for l in lines]


def is_symbol(c):
    return c not in ".0123456789 "
    # return c == "*"


def is_number(col, row):
    return chars[row][col] in "0123456789"

def is_adjacent(col, row):
    adjacents = ""
    if col > 0:
        adjacents += chars[row][col - 1]
        if row > 0:
            adjacents += chars[row - 1][col - 1]
        if row < len(chars) - 1:
            adjacents += chars[row + 1][col - 1]
    if col < len(chars[0]) - 1:
        adjacents += chars[row][col + 1]
        if row > 0:
            adjacents += chars[row - 1][col + 1]
        if row < len(chars) - 1:
            adjacents += chars[row + 1][col + 1]
    if row > 0:
        adjacents += chars[row - 1][col]
    if row < len(chars) - 1:
        adjacents += chars[row + 1][col]
    return any(is_symbol(c) for c in adjacents)

mask = [
    [
        c if is_number(i, j) and is_adjacent(i, j) else ' '
        for (i, c) in enumerate(l)
    ]
    for (j, l) in enumerate(chars)
]

for _ in range(3):
    for row, mask_row in enumerate(mask):
        l = len(mask_row)
        for col, v in enumerate(mask_row):
            if is_number(col, row) and v == ' ' and (
                (col > 0 and mask_row[col - 1] != ' ') or (col < l - 1 and mask_row[col + 1] != ' ')
            ):
                mask[row][col] = chars[row][col]

# print('\n'.join(''.join(mask_row) for mask_row in mask))
# print(repr(chars[0][-1]))
# types = []
# for row in range(len(chars)):
#     t_row = []
#     for col in range(len(chars[row])):
#         if chars[row][col] == mask[row][col]:
#             t_row.append('P')
#         elif is_number(col, row):
#             t_row.append('N')
#         elif chars[row][col] == '.':
#             t_row.append(' ')
#         else:
#             t_row.append('X')
#     types.append(t_row)
# print('\n'.join(''.join(r) for r in types))


parts = ' '.join(''.join(mask_row) for mask_row in mask)
part_total = sum(int(v) for v in parts.split(' ') if v)
print(part_total)

part_map = {}


def get_row_ids(r, i):
    next_id = (i + 1) * 1000
    last_part = ''
    out = []
    for v in r:
        if v == ' ':
            if last_part:
                part_map[next_id] = int(last_part)
                last_part = ''
            next_id += 1
            out.append(0)
        else:
            last_part += v
            out.append(next_id)

    if last_part:
        part_map[next_id] = int(last_part)

    return out


part_ids = [get_row_ids(r, i) for i, r in enumerate(mask)]

gear_sum = 0

for row, char_row in enumerate(chars):
    for col, char in enumerate(char_row):
        if char == "*":
            adjacent_ids = set()
            if col > 0:
                adjacent_ids.add(part_ids[row][col - 1])
                if row > 0:
                    adjacent_ids.add(part_ids[row - 1][col - 1])
                if row < len(chars) - 1:
                    adjacent_ids.add(part_ids[row + 1][col - 1])
            if col < len(chars[0]) - 1:
                adjacent_ids.add(part_ids[row][col + 1])
                if row > 0:
                    adjacent_ids.add(part_ids[row - 1][col + 1])
                if row < len(chars) - 1:
                    adjacent_ids.add(part_ids[row + 1][col + 1])
            if row > 0:
                adjacent_ids.add(part_ids[row - 1][col])
            if row < len(chars) - 1:
                adjacent_ids.add(part_ids[row + 1][col])
            adjacent_ids -= {0}
            if len(adjacent_ids) == 2:
                gear_ratio = 1
                parts = []
                for part_id in adjacent_ids:
                    gear_ratio *= part_map[part_id]
                    parts.append(part_map[part_id])
                print(row, col, parts, gear_ratio)
                gear_sum += gear_ratio

print(gear_sum)
