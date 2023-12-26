import time
import sys

t0 = time.time()
base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

seed_inputs = [int(s) for s in lines[0].split(":")[1].split(" ") if s]

seed_starts = seed_inputs[::2]
seed_lens = seed_inputs[1::2]

maps = []
map_names = []
next_map = []
for line in lines[2:]:
    if "map" in line:
        map_names.append(line.split(" ")[0])
    elif not line:
        maps.append(next_map)
        next_map = []
    else:
        next_map.append([int(v) for v in line.split() if v])
if next_map:
    maps.append(next_map)

assert len(map_names) == len(maps)
# print(list(zip(map_names, maps)))

def follow_map(v, m):
    for out0, in0, n in m:
        if v >= in0 and v < in0 + n:
            return v + out0 - in0
    return v


def follow_all(v):
    out = [v]
    for m in maps:
        v = follow_map(v, m)
        out.append(v)
    return v

# this was part 1
# locations = [follow_all(v) for v in seeds]
# print(min(locations))


def make_pair(v):
    return (v, follow_all(v))


def interpolate_once(pairs):
    pairs_out = [pairs[0]]
    for i in range(1, len(pairs)):
        inprev, outprev = pairs[i - 1]
        ini, outi = pairs[i]
        # this is the key: if the input & output spans are different,
        # we must have crossed a map boundary, so split the difference
        # after we've found all the map boundaries, the min must be the
        # first after one of the boundaries
        if ini - inprev > 1 and outi - outprev != ini - inprev:
            innew = (ini + inprev)//2
            pairs_out.append(make_pair(innew))
        pairs_out.append(pairs[i])
    return pairs_out


def interpolate_all(pairs):
    pairs_out = interpolate_once(pairs)
    if len(pairs) == len(pairs_out):
        return pairs
    return interpolate_all(pairs_out)


def min_in_range(s0, sl):
    pairs = interpolate_all([make_pair(s0), make_pair(s0 + sl - 1)])
    print(len(pairs))  # how many seeds did we have to calculate for this range?
    outputs = [p[1] for p in pairs]
    return min(outputs)


all_mins = [min_in_range(s0, sl) for s0, sl in zip(seed_starts, seed_lens)]
print(min(all_mins))
t1 = time.time()
print(t1-t0)
