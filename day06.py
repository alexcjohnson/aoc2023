import math
import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

# remove the next line for part 1
lines = [l.replace(" ", "") for l in lines]

times = [int(v) for v in lines[0].split(":")[1].split(" ") if v]
distances = [int(v) for v in lines[1].split(":")[1].split(" ") if v]

prod = 1
for time, distance in zip(times, distances):
    disc = (time**2 - 4 * distance) ** 0.5
    hmin = math.floor((time - disc) / 2) + 1
    hmax = math.ceil((time + disc) / 2) - 1
    prod *= (hmax - hmin + 1)

print(prod)
