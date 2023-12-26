import sys
import time

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]


def rollOneV(from_line, to_line):
    from_out, to_out = "", ""
    for f, t in zip(from_line, to_line):
        if f == "O" and t == ".":
            from_out += "."
            to_out += "O"
        else:
            from_out += f
            to_out += t

    return from_out, to_out, from_out == to_out

def _rollV(north):  # original implementation - transpose and rollH is way faster!
    for _ in range(len(lines)):
        no_rolls_this_cycle = True
        for i in range(len(lines) - 1):
            fromi, toi = (i + 1, i) if north else (len(lines) - i - 2, len(lines) - i - 1)
            lines[fromi], lines[toi], no_rolls = rollOneV(lines[fromi], lines[toi])
            no_rolls_this_cycle = no_rolls_this_cycle and no_rolls
        if no_rolls_this_cycle:
            break


def rollH(west):
    for i in range(len(lines)):
        line = lines[i] if west else "".join(list(reversed(lines[i])))
        out = ""
        dots = ""
        for char in line:
            if char == ".":
                dots += "."
            elif char == "O":
                out += "O"
            else:
                out += dots + char
                dots = ""
        out += dots
        lines[i] = out if west else "".join(list(reversed(out)))


def transpose(block):
    return ["".join(row[i] for row in block) for i in range(len(block[0]))]


def rollV(north):
    lines[:] = transpose(lines)
    rollH(north)
    lines[:] = transpose(lines)


def calc_sum():
    return sum((len(lines) - i) * line.count("O") for i, line in enumerate(lines))

t0 = time.time()
prev_lines = ["".join(lines)]
sums = [calc_sum()]
for i in range(1, 1000):
    rollV(True)
    rollH(True)
    rollV(False)
    rollH(False)
    new_sum = calc_sum()
    new_lines = "".join(lines)
    if new_lines in prev_lines:
        i0 = prev_lines.index(new_lines)
        period = i - i0
        end_reduced = ((1000000000 - i) % period) + i - period
        print(f"period: {period}, iterations: {i}, sum at 1000000000: {sums[end_reduced]}")
        print(i, i0, new_sum, sums[i0:])
        break
    prev_lines.append(new_lines)
    sums.append(new_sum)
else:
    print(f"did not repeat after {i} iterations")

print(time.time() - t0)
