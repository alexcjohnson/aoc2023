# If I had thought of the calculus-based approach from the beginning... here's how short day 18 could have been
import sys

base = __file__.split("/")[-1].split(".")[0][:5]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip().split(" ") for l in f.readlines()]

x, y = 0, 0
dirmap = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
area = 0
perimeter = 0
for a, b, c in lines:
    dist, angle = int(c[2:-2], 16), "RDLU"[int(c[-2])]  # part 2
    # dist, angle = int(b), a  # part 1
    vec = dirmap[angle]
    x += dist * vec[1]
    y += dist * vec[0]
    area += x * dist * vec[0]
    perimeter += dist

print(abs(area) + (perimeter//2) + 1)
