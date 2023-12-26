import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

locs = [[int(char) for char in line] for line in lines]
visited = [[set() for _ in line] for line in lines]
max_row = len(locs) - 1
max_col = len(locs[0]) - 1

# path, end_pos, score
paths = [[[(0, 1)], (0, 1), locs[0][1]], [[(1, 0)], (1, 0), locs[1][0]]]
# grid of sets: {(dr, dc, reps)}
visited[0][1].add((0, 1, 1))
visited[1][0].add((1, 0, 1))

final_score = 1e100
part = 2

while paths:
    new_paths = []
    min_score = min(path[2] for path in paths)
    print(len(paths), min_score)
    for path_info in paths:
        if path_info[2] != min_score:
            new_paths.append(path_info)
            continue
        path, pos, score = path_info
        r, c = pos
        reps_now = 1
        for i in range(len(path) - 1):
            if path[-i-1] == path[-i-2]:
                reps_now += 1
            else:
                break
        # next_steps = [(1, 0), (-1, 0)] if path[-1][1] else [(0, 1), (0, -1)]  # part 1
        next_steps = ([(1, 0), (-1, 0)] if path[-1][1] else [(0, 1), (0, -1)]) if (part == 1 or reps_now > 3) else []  # part 2
        # if reps_now < 3:  # part 1
        if reps_now < (3 if part == 1 else 10):  # part 2
            next_steps.append(path[-1])
        for dr, dc in next_steps:
            new_r = r + dr
            new_c = c + dc
            if new_r < 0 or new_r > max_row or new_c < 0 or new_c > max_col:
                continue
            new_score = score + locs[new_r][new_c]
            if new_score > final_score:
                continue
            reps = 1 + (reps_now if (dr, dc) == path[-1] else 0)
            prev_scores = visited[new_r][new_c]
            if (dr, dc, reps) in visited[new_r][new_c]:
                # because we're searching from the lowest score only,
                # if we've been here before with the same direction and reps
                # that must have been a better route and we can terminate this route.
                continue
            if new_r == max_row and new_c == max_col:
                if new_score > final_score:
                    break
                if part == 2 and reps < 4:  # part 2
                    break
                final_score = new_score
                output = [[" " for _ in line] for line in lines]
                r, c = 0, 0
                real_score = 0
                for dr, dc in path + [(dr, dc)]:
                    r += dr
                    c += dc
                    real_score += locs[r][c]
                    output[r][c] = lines[r][c]
                assert real_score == new_score  # sanity check
                break
            prev_scores.add((dr, dc, reps))
            new_paths.append([path + [(dr, dc)], (new_r, new_c), new_score])
    paths = new_paths

for r in range(len(output)):
    for c in range(len(output[0])):
        if visited[r][c] and output[r][c] == " ":
            output[r][c] = "."  # show which squares were visited at all
print("\n".join("".join(row) for row in output))
print(final_score)
