import math
import re
import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{('test' + sys.argv[-1]) if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

seq = [0 if v=="L" else 1 for v in lines[0]]

net = {}
for line in lines[2:]:
    node, left, right = re.match(r"^([A-Z0-9]+) = \(([A-Z0-9]+), ([A-Z0-9]+)\)$", line).groups()
    net[node] = (left, right)

# steps = 0
# loc = "AAA"
locs = [n for n in net if n[-1] == "A"]
routes = []
zs = []
prod = []

for start_loc in locs:
    loc = start_loc
    route = []
    loops = 0
    while True:
        for s in seq:
            route.append(loc)
            loc = net[loc][s]
        loops += 1
        if loops > 1 and loc in route[::len(seq)]:
            break
    start = route[::len(seq)].index(loc) * len(seq)
    adjusted_route = (route[-start:] + route[start: -start]) if start else route
    routes.append(adjusted_route)
    zs.append("".join("Z" if loc[-1] == "Z" else " " for loc in adjusted_route))
    print(zs[-1].count("Z"), zs[-1].index("Z"))
    print(len(route), start, len(seq), len(adjusted_route))
    prod.append(len(adjusted_route))

print(math.lcm(*prod))

# while loc != "ZZZ":
    # loc = net[loc][seq[steps % len(seq)]]
    # steps += 1

# print(steps)
