import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip().split(" ") for l in f.readlines()]

# part 2
for line in lines:
    line[1], line[0] = int(line[2][2:-2], 16), "RDLU"[int(line[2][-2])]  # part 2
    # line[1] = int(line[1])  # part 1

x, minx, maxx, y, miny, maxy = [0] * 6
xset, yset = set([0]), set([0])
dirmap = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
area = 0
perimeter = 0
for angle, dist, _ in lines:
    vec = dirmap[angle]
    x += dist * vec[1]
    y += dist * vec[0]
    xset.add(x)
    yset.add(y)
    minx = min(x, minx)
    maxx = max(x, maxx)
    miny = min(y, miny)
    maxy = max(y, maxy)
    area += x * dist * vec[0]
    perimeter += dist
# OK now I feel dumb... could have been done right here, no need to actually draw the grid
# area counts from the centerline of each dig, so add perimeter/2 to get the dig itself
# plus 1 for the net 4 outer corners in the loop
print(abs(area) + (perimeter//2) + 1)

def makemap(s):
    ss = sorted(s)
    outpos, outsize = [ss[0]], [1]
    prevpos = ss[0]
    for si in ss[1:]:
        if si > prevpos + 1:
            outpos.append(prevpos + 1)
            outsize.append(si - prevpos - 1)
        outpos.append(si)
        outsize.append(1)
        prevpos = si
    return outpos, outsize

xmap, xsize = makemap(xset)
ymap, ysize = makemap(yset)

# grid = [["." for _ in range(maxx - minx + 1)] for _ in range(maxy - miny + 1)]  # part 1
# x, y = -minx, -miny  # part 1
grid = [["." for _ in xmap] for _ in ymap]  # part 2
x, y = xmap.index(0), ymap.index(0)  # part 2
grid[y][x] = "#"
for angle, dist, _ in lines:
    vec = dirmap[angle]
    mapdx = xmap.index(xmap[x] + dist * vec[1]) - x if vec[1] else 0  # part 2
    mapdy = ymap.index(ymap[y] + dist * vec[0]) - y if vec[0] else 0  # part 2
    mapdist = abs(mapdx + mapdy)  # part 2
    for _ in range(mapdist):  # part 2 - for 1 use dist
        x += vec[1]
        y += vec[0]
        grid[y][x] = "#"

for i in range(len(grid) - 2):
    row1, row2 = grid[i], grid[i + 1]
    inside = False
    for j in range(len(row1)):
        c1, c2 = row1[j], row2[j]
        if c1 == "#" and c2 == "#":
            inside = not inside
        elif c2 == "." and inside:
            row2[j] = "X"

# print("\n".join("".join(row) for row in grid))
# print(sum(sum(0 if c == "." else 1 for c in row) for row in grid))  # part 1

# part 2
total = 0
for row, rowsize in zip(grid, ysize):
    for c, colsize in zip(row, xsize):
        if c != ".":
            total += rowsize * colsize
print(total)
