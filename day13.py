import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

blocks = []
nextblock = []
for line in lines:
    if line:
        nextblock.append(line)
    else:
        blocks.append(nextblock)
        nextblock = []
blocks.append(nextblock)


def mismatch(s1, s2):
    return sum(1 if a!=b else 0 for (a, b) in zip(s1, s2))


def find_reflection_row(block, errors_expected):
    for i in range(len(block) - 1):
        errors = mismatch(block[i], block[i + 1])
        if errors <= errors_expected:
            for j, k in zip(reversed(range(i)), range(i+2, len(block))):
                errors += mismatch(block[j], block[k])
                if errors > errors_expected:
                    break
            else:
                if errors == errors_expected:
                    return i + 1
    return 0


def transpose(block):
    return ["".join(row[i] for row in block) for i in range(len(block[0]))]


total = 0
for block in blocks:
    total += 100 * find_reflection_row(block, 1)
    total += find_reflection_row(transpose(block), 1)

print(total)
