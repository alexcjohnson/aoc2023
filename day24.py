import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

xymin, xymax = (7, 27) if 't' in sys.argv else (200000000000000, 400000000000000)

positions, velocities, slopes, yints = ([], [], [], [])
for line in lines:
    ps, vs = line.split(" @ ")
    pi = [int(v) for v in ps.split(", ")]
    vi = [int(v) for v in vs.split(", ")]
    positions.append(pi)
    velocities.append(vi)
    # y = (vy/vx)*x + (py*vx - px*vy)/vx
    # there are no zeros in either positions or velocities
    slopes.append(vi[1] / vi[0])
    yints.append((pi[1] * vi[0] - pi[0] * vi[1])/vi[0])

collisions = 0
for i in range(len(lines)):
    for j in range(i + 1, len(lines)):
        si, sj = slopes[i], slopes[j]
        ii, ij = yints[i], yints[j]
        if si == sj:
            continue
        x = (ij - ii) / (si - sj)
        if x < xymin or x > xymax:
            continue
        y = si * x + ii
        if y < xymin or y > xymax:
            continue
        ti = (x - positions[i][0]) / velocities[i][0]
        if ti < 0:
            continue
        tj = (x - positions[j][0]) / velocities[j][0]
        if tj < 0:
            continue
        collisions += 1

print("part 1:", collisions)  # part 1 answer

# for part 2, you only need to look at the first three hailstones, the others must be right
# from hailstone 0 at t0 to 1 at t1 and 2 at t2, we can calculate the rock velocity (3 ways, 2 independent),
# and find times t0, t1, t2 that make those velocities match
# (p1 + v1*t1 - (p0 + v0*t0))/(t1 - t0) = vr
# (p2 + v2*t2 - (p0 + v0*t0))/(t2 - t0) = vr


def find_v(i, j, ti, tj):
    p0, p1 = positions[i], positions[j]
    v0, v1 = velocities[i], velocities[j]
    return [(p1[i] + v1[i] * tj - (p0[i] + v0[i] * ti)) / (tj - ti) for i in [0, 1, 2]]


def find_error(t0, t1, t2):
    v01 = find_v(0, 1, t0, t1)
    v02 = find_v(0, 2, t0, t2)
    v12 = find_v(1, 2, t1, t2)
    return sum(max((v01[i] - v02[i])**2, (v01[i] - v12[i])**2, (v02[i] - v12[i])**2) for i in [0, 1, 2])


# the times will be up to on the order of 10^12 or so
# first find the best triplet on a big grid, then slowly zoom in on that best point.
center = [10, 11, 12] if 't' in sys.argv else [500000000000, 501000000000, 502000000000]
diff = center[0]/7
step = 0
while diff > 0.2:
    step += 1
    best = center
    best_err = find_error(*center)
    for i in range(-10, 11):
        t0 = center[0] + i * diff
        for j in range(-10, 11):
            t1 = center[1] + j * diff
            for k in range(-10, 11):
                t2 = center[2] + k * diff
                new_err = find_error(t0, t1, t2)
                if new_err < best_err:
                    best_err = new_err
                    best = [t0, t1, t2]
    center = best
    diff /= 1.2
    if not step % 10:
        print(f"step {step}, diff {diff:.1f}, err {best_err:.1f}, best: {[round(v) for v in best]}")

final_t = [int(round(v)) for v in best]
print(find_error(*final_t))

final_v = find_v(0, 1, final_t[0], final_t[1])
rock_start = [positions[0][i] + (velocities[0][i] - int(final_v[i])) * final_t[0] for i in [0, 1, 2]]
print("part 2:", sum(rock_start))
