from functools import cache
import time
import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]


def find_seqs(seq, target):
    seqlen = len(seq)
    targetlen = len(target)
    starting_min = seq.count("#")
    starting_max = starting_min + seq.count("?")

    # LOL I did so much optimization below, but cache is really all I needed
    # to go from can't-do-line-32-in-an-hour to all-done-under-a-sec
    @cache
    def find_inner(seqi, targeti, remaining_max, remaining_min, target_sum):
        next_raw = seq[seqi]
        wild = next_raw == "?"
        next_chars = "#." if wild else next_raw
        out = 0
        for next_char in next_chars:
            new_targeti = targeti
            step = 1
            new_sum = target_sum
            newi = seqi + 1
            if next_char == ".":
                if wild and new_sum >= remaining_max:
                    continue
                new_remain_max = remaining_max - (1 if next_raw != "." else 0)
                new_remain_min = remaining_min
            else:
                step = target[targeti]
                newi = seqi + step
                stepseq = seq[seqi:newi]
                if  "." in stepseq or newi > seqlen:
                    continue
                if newi == seqlen:
                    if targeti == targetlen - 1:
                        out += 1
                    continue
                if seq[newi] == "#":
                    continue
                stepseq += seq[newi]
                step += 1
                newi += 1
                new_targeti += 1
                new_sum -= target[targeti]

                if new_targeti == targetlen:
                    if "#" not in seq[newi:] and not new_sum:
                        out += 1
                    continue

                new_remain_max = remaining_max - step + stepseq.count(".")
                new_remain_min = remaining_min - stepseq.count("#")

                if new_remain_min > new_sum:
                    continue  # we have too many known damaged pieces left for the remaining target

            if new_sum + targetlen - new_targeti - 1 > seqlen - newi:
                continue  # to match the target we need more pieces of any kind than remain

            out += find_inner(newi, new_targeti, new_remain_max, new_remain_min, new_sum)

        return out

    return find_inner(0, 0, starting_max, starting_min, sum(target))

total = 0
t00 = time.time()
for i, line in list(enumerate(lines)):
    s, target_str = line.split(" ")
    target = [int(i) for i in target_str.split(",")]
    s2 = "?".join([s] * 5)
    target2 = target * 5
    # s2, target2 = s, target  # part 1
    s2 = s2.replace("..", ".").strip(".")
    t0 = time.time()
    seq_count = find_seqs(s2, target2)
    t1 = time.time()
    # print(f"{i+1}: {seq_count} --- {t1 - t0:.3f} --- {s} {target}")
    total += seq_count

print(f"{total} - {time.time() - t00} sec")
