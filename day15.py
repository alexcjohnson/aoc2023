import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]


def h(s):
    out = 0
    for c in s:
        out = (17 * (out + ord(c))) % 256
    return out

seq = "".join(lines).split(",")

print(sum(h(si) for si in seq))  # part 1

boxes = [{} for i in range(256)]

for si in seq:
    if si[-1] == "-":
        label = si[:-1]
        box = boxes[h(label)]
        if label in box:
            del box[label]
    else:
        label = si[:-2]
        box = boxes[h(label)]
        box[label] = int(si[-1])

fp = 0
for boxi, box in enumerate(boxes):
    for lensi, f in enumerate(box.values()):
        fp += (boxi + 1) * (lensi + 1) * f

print(fp)  # part 2 - conveniently Py3 dicts maintain order exactly as required for this problem
