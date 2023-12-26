import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

module_outputs, ff_state, conj_state = {}, {}, {}
for line in lines:
    fullname, outputstr = line.split(" -> ")
    outputs = outputstr.split(", ")
    if fullname == "broadcaster":
        broadcast_to = outputs
        continue
    mod_type, mod_name = fullname[0], fullname[1:]
    module_outputs[mod_name] = outputs
    if mod_type == "%":
        ff_state[mod_name] = "off"
    else:
        conj_state[mod_name] = {}

for mod_name, outputs in module_outputs.items():
    for output in outputs:
        if output in conj_state:
            conj_state[output][mod_name] = "low"

# part 2: hp is the only one that sends pulses to rx, so find what triggers hp and when this is high
hp_triggers = {k: set() for k in conj_state["hp"]}


pulse_queue = []
pulse_count = {"low": 0, "high": 0, "buttons": 0, "rxlow": 0}


def add_pulses(to_name, new_pulse):
    pulse_queue.extend((to_name, new_pulse, output) for output in module_outputs[to_name])
    if to_name == "rx" and new_pulse == "low":
        pulse_count["rxlow"] += 1


def handle_pulse():
    from_name, pulse_state, to_name = pulse_queue.pop(0)
    pulse_count[pulse_state] += 1
    if to_name in ff_state:
        if pulse_state == "low":
            new_pulse, ff_state[to_name] = ("high", "on") if ff_state[to_name] == "off" else ("low", "off")
            add_pulses(to_name, new_pulse)
    elif to_name in conj_state:
        cs = conj_state[to_name]
        cs[from_name] = pulse_state
        new_pulse = "low" if all(v == "high" for v in cs.values()) else "high"
        add_pulses(to_name, new_pulse)
        if to_name == "hp":
            for n in cs:
                if cs[n] == "high":
                    hp_triggers[n].add(pulse_count["buttons"])


def press_button():
    pulse_count["low"] += 1
    pulse_count["buttons"] += 1
    pulse_queue.extend(("b", "low", output) for output in broadcast_to)
    while pulse_queue:
        handle_pulse()


for _ in range(100000):  # for part 1 set to 1000
    press_button()
    if pulse_count["rxlow"]:  # part 2: of course the brute force approach wouldn't work!
        print(f'\n{pulse_count["rxlow"]} {pulse_count["buttons"]}\n')

print(f"\n{pulse_count}")  # part 1, with 1000 button presses
for k, v in hp_triggers.items():
    print(k, sorted(v))

# yields a list of times the inputs to hp are high:
#   sr [3923, 7846, 11769, 15692, 19615, 23538, 27461, 31384, 35307, 39230, 43153, 47076, 50999, 54922, 58845, 62768, 66691, 70614, 74537, 78460, 82383, 86306, 90229, 94152, 98075]
#   sn [3967, 7934, 11901, 15868, 19835, 23802, 27769, 31736, 35703, 39670, 43637, 47604, 51571, 55538, 59505, 63472, 67439, 71406, 75373, 79340, 83307, 87274, 91241, 95208, 99175]
#   rf [4021, 8042, 12063, 16084, 20105, 24126, 28147, 32168, 36189, 40210, 44231, 48252, 52273, 56294, 60315, 64336, 68357, 72378, 76399, 80420, 84441, 88462, 92483, 96504]
#   vq [3917, 7834, 11751, 15668, 19585, 23502, 27419, 31336, 35253, 39170, 43087, 47004, 50921, 54838, 58755, 62672, 66589, 70506, 74423, 78340, 82257, 86174, 90091, 94008, 97925]
# which shows that all are periodic, with different periods, and high exactly at the end of their periods.
# assuming these are all mutually prime, the first time they're all high together is their product:
#   245114020323037
# and this was the accepted answer so I guess they are indeed mutually prime :)
