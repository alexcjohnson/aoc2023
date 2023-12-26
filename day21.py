import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

chars_orig = [[c for c in l] for l in lines]

extra_chars = [["." if c == "S" else c for c in l] for l in chars_orig]

n_extra = 7

chars = (
    [row * (2 * n_extra + 1) for _ in range(n_extra) for row in extra_chars] +
    [(erow * n_extra) + orow + (erow * n_extra) for erow, orow in zip(extra_chars, chars_orig)] +
    [row * (2 * n_extra + 1) for _ in range(n_extra) for row in extra_chars]
)

maxrow = len(chars) - 1
maxcol = len(chars[0]) - 1


def iterate(n):
    prev_char = "S" if n % 2 else "O"
    new_char = "O" if n % 2 else "S"
    center = len(chars) // 2
    first_row = center - n
    last_row = center + n
    for row in range(first_row, last_row + 1):
        extent = min(row - first_row, last_row - row)
        for col in range(center - extent, center + extent + 1):
            if chars[row][col] == ".":
                if (
                    (row and chars[row - 1][col] == prev_char) or
                    (col and chars[row][col - 1] == prev_char) or
                    (row < maxrow and chars[row + 1][col] == prev_char) or
                    (col < maxcol and chars[row][col + 1] == prev_char)
                ):
                    chars[row][col] = new_char


target = 26501365
tmod = target % len(chars_orig)
tfinal = tmod + len(chars_orig) * 6

fn = []
for i in range(1, tfinal + 1):
    iterate(i)
    if i % (2 * len(chars_orig)) == 65:
        total = sum(sum(1 if c == "O" else 0 for c in l) for l in chars)
        print(f"\n{i}: {total}\n")
        fn.append(total)
    else:
        print(i % 10, end=" ", flush=True)

# total = sum(sum(1 if c == "S" else 0 for c in l) for l in chars)
# print(total)  # part 1

# part 2: how many squares can you get to on an infinitely-repeating grid like this in 26501365 steps?
# the input grid is 131 chars wide and tall, 26501365 is 202300 * 131 + 65
# 65: 3776 = f(0)
# 327 = 65 + 262*1: 257253 = f(1)
# 589 = 65 + 262*2: 584415 = f(2)
# what is f(101150)?
# f(n) = an^2 + bn + c
# f0 = c
# f1 = a + b + c
# f2 = 4a + 2b + c
# f1-f0 = a+b
# f2-f1 = 3a+b
# f2+f0-2f1 = 2a -> a = (f0+f2)/2 - f1
# b = f1-f0 - f0/2 - f2/2 + f1 = 2f1 - 3f0/2 - f2/2
c = fn[0]
a = (c + fn[2])//2 - fn[1]
b = fn[1] - a - c
f_3_predicted = a * 9 + b * 3 + c  # to verify that the sequence is quadratic, test the next value
print(f_3_predicted, fn[3], f_3_predicted == fn[3])
nf = 101150
f_final = a * nf * nf + b * nf + c
print(f"final after 26501365 steps: {f_final}")
