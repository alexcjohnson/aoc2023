s = 0
digit_text = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "zero": 0
}
for d in list(digit_text.values()):
    digit_text[str(d)] = d
with open("day01input.txt", "r", encoding="utf-8") as f:
    for line in f:
        # digits = [int(char) for char in line if char in '0123456789']
        # first_d, last_d = digits[0], digits[-1]
        first_index = len(line)
        last_index = -1
        first_d = 0
        last_d = 0
        for txt, d in digit_text.items():
            first_txt, last_txt = line.find(txt), line.rfind(txt)
            if first_txt != -1:
                if first_txt < first_index:
                    first_index = first_txt
                    first_d = d
                if last_txt > last_index:
                    last_index = last_txt
                    last_d = d
        s += (first_d * 10) + last_d
print(s)
