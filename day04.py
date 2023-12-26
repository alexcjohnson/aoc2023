import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    cards = [l.strip() for l in f.readlines()]

total = 0
card_wins = {}
card_copies = [0] * (len(cards) + 1)
for card in cards:
    head, nums = card.strip().split(":")
    card_num = int(head.split(" ")[-1])
    wins_str, mine_str = nums.split("|")
    wins = set([n for n in wins_str.split(" ") if n])
    mine = set([n for n in mine_str.split(" ") if n])
    my_wins = mine.intersection(wins)
    card_wins[card_num] = len(my_wins)
    card_copies[card_num] = 1
    if my_wins:
        total += 2**(len(my_wins) - 1)

print(total)

for i in range(1, len(card_copies)):
    for j in range(i + 1, i + 1 + card_wins[i]):
        if j < len(card_copies):
            card_copies[j] += card_copies[i]

print(sum(card_copies))
