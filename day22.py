import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

specs = [[[int(c) for c in end.split(",")] for end in l.split("~")] for l in lines]

spans = [(min(b[i] for s in specs for b in s), max(b[i] for s in specs for b in s) + 1) for i in range(3)]
specs.sort(key=lambda s: s[0][2])

z_fixed = [[0 for _ in range(*spans[0])] for _ in range(*spans[1])]


def fall(i):
    brick = specs[i]
    fixed_below = [row[brick[0][0]: brick[1][0] + 1] for row in z_fixed[brick[0][1]: brick[1][1] + 1]]
    new_z0 = max(i for row in fixed_below for i in row) + 1
    new_z1 = new_z0 + brick[1][2] - brick[0][2]
    brick[0][2], brick[1][2] = new_z0, new_z1
    for x in range(brick[0][0], brick[1][0] + 1):
        for y in range(brick[0][1], brick[1][1] + 1):
            z_fixed[y][x] = new_z1


for i in range(len(specs)):
    if any(specs[i][0][j]>specs[i][1][j] for j in range(3)):
        print("misordered")  # nope, all ordered :) - that makes the rest of the logic work
    fall(i)

print(z_fixed)

supported_by = [[] for _ in specs]
for i, bi in enumerate(specs):
    for j, bj in enumerate(specs[:i]):
        if (
            bj[1][0] >= bi[0][0] and bj[0][0] <= bi[1][0] and
            bj[1][1] >= bi[0][1] and bj[0][1] <= bi[1][1] and
            bi[0][2] == bj[1][2] + 1
        ):
            supported_by[i].append(j)

only_support = set()
for si in supported_by:
    if len(si) == 1:
        only_support.add(si[0])

print("bricks that cause no others to fall:", len(specs) - len(only_support))  # part 1

# part 2
total = 0
for i in only_support:
    removed = [i]
    for j, sj in enumerate(supported_by):
        if j > i and len(sj) and all(sjk in removed for sjk in sj):
            removed.append(j)
    total += len(removed) - 1

print("part 2 total:", total)
