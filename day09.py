import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

seqs = [[int(v) for v in l.split(" ") if v] for l in lines if l]


def extrapolate(seq):
    if any(seq):
        diffs = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
        next_diff = extrapolate(diffs)
        # return seq[-1] + next_diff  # part 1
        return seq[0] - next_diff  # part 2
    return 0


print(sum(extrapolate(s) for s in seqs))
