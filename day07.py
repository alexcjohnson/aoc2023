import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]


translate = dict(zip("AKQT98765432J", "abcdefghijklm"))
ranks = [(5,), (4,1), (3,2), (3,1,1), (2,2,1), (2,1,1,1), (1,1,1,1,1)]

def analyze_hand(raw_hand, raw_bid):
    hand = [translate[c] for c in raw_hand]
    cards_found = set(hand) - set([translate["J"]])
    card_counts = tuple(sorted([hand.count(c) for c in cards_found], reverse=True))
    if "J" in raw_hand:
        if not card_counts:
            card_counts = (5,)  # all jokers
        else:
            card_counts = (card_counts[0] + raw_hand.count("J"),) + card_counts[1:]
    return [ranks.index(card_counts)] + hand + [int(raw_bid)]


hands = sorted([analyze_hand(*l.split(" ")) for l in lines if l], reverse=True)
for h in hands:
    print(h)
print(sum([(i + 1) * h[-1] for i, h in enumerate(hands)]))
