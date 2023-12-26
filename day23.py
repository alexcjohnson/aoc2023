import sys
import time

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

lastline = len(lines) - 1
start = (0, 1)
end = (lastline, lines[-1].index("."))
longest_path = None
max_len = 0
t0 = time.time()


def get_next(pos, prevpos=None):  # to change between part 1 & 2 just flip the 4 commented lines below
    y, x = pos
    return [
        next_pos
        # for next_pos, goodslope in zip(((y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)), "^<>v")  # part 1
        for next_pos in ((y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x))  # part 2
        if next_pos != prevpos and
        # (lines[next_pos[0]][next_pos[1]] in ("." + goodslope if prevpos else ".^<>v"))  # part 1
        lines[next_pos[0]][next_pos[1]] != "#"  # part 2
    ]


junctions = []
for y in range(1, lastline):
    for x in range(1, len(lines[0]) - 1):
        if lines[y][x] == "." and len(get_next((y, x))) > 2:
            junctions.append((y,x))
segments = {}

segment_ends = junctions + [start, end]

for pos in junctions + [start]:
    starts = [(1, 1)] if pos == start else get_next(pos)
    pos_segments = {}
    for starti in starts:
        segmentlen = 1
        next_pos = starti
        prev_pos = pos
        while next_pos not in segment_ends:
            try:
                prev_pos, next_pos = next_pos, get_next(next_pos, prev_pos)[0]
            except:
                next_pos = None
                break
            segmentlen += 1
        if not next_pos:
            continue
        if pos == start:
            start_len = segmentlen
            start_junction = next_pos
        elif next_pos == end:
            end_len = segmentlen
            end_junction = pos
        elif next_pos != start:
            pos_segments[next_pos] = segmentlen
    segments[pos] = pos_segments

print(f"start: {start_junction}, +{start_len} to entry, end: {end_junction}, +{end_len} to exit, junctions: {len(junctions)}")

paths = [(start_junction,)]
finishing_paths = 0
while paths:
    new_paths = []
    print(f"internal segments: {len(paths[0]) - 1}, paths in progress: {len(paths)}, max len: {max_len + start_len + end_len}, paths finished: {finishing_paths}, {time.time() - t0:.3f} secs")
    for path in paths:
        if path[-1] == end_junction:
            finishing_paths += 1
            path_len = sum(segments[path[i]][path[i + 1]] for i in range(len(path) - 1))
            if path_len > max_len:
                max_len = path_len
                longest_path = path
            continue
        for next_pos in segments[path[-1]]:
            if next_pos not in path:
                new_paths.append(path + (next_pos,))
    paths = new_paths

print(f"max length with start and end: {max_len + start_len + end_len}, total time: {time.time() - t0:.3f}, {finishing_paths} paths finished")
# part 1 ran in ~60ms, evaluated 252 paths at peak, and 252 paths finished
# part 2 ran in ~43 sec, evaluated 2161710 paths at peak, and 1262816 paths finished
# if we use lists instead of tuples for paths, part 2 takes 57 sec
