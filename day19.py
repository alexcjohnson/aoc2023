import sys

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

rulestrs = [line for line in lines if line and line[0] != "{"]
rules = {}
for rulestr in rulestrs:
    rn, t = rulestr[:-1].split("{")
    teststrs = [ti.split(":") for ti in t.split(",")]
    tests = [
        {"k": ti[0][0], "op": ti[0][1], "v": int(ti[0][2:]), "target": ti[1]}
        if len(ti)==2 else
        {"k": "x", "op": ">", "v": 0, "target": ti[0]}
        for ti in teststrs
    ]
    rules[rn] = tests

# partstrs  = [line for line in lines if line and line[0] == "{"]
# parts = [dict([(i.split("=")[0], int(i.split("=")[1])) for i in p[1:-1].split(",")]) for p in partstrs]

# vals = {"x": set([1, 4000]), "m": set([1, 4000]), "a": set([1, 4000]), "s": set([1, 4000])}
# for tests in rules.values():
#     for test in tests:
#         if test["v"]:
#             vals[test["k"]].add(test["v"] + (1 if test["op"] == ">" else 0))
# for k in list(vals.keys()):

ops = {
    ">": lambda a, b: a > b,
    "<": lambda a, b: a < b
}

# total = 0
# for part in parts:
#     wf = "in"
#     for _ in range(len(rules)):
#         for test in rules[wf]:
#             if ops[test["op"]](part[test["k"]], test["v"]):
#                 wf = test["target"]
#                 break
#         if wf in ["A", "R"]:
#             if wf == "A":
#                 total += sum(part.values())
#             break

# print(total)


def propagate(rng, wf):
    total = 0
    rng_next = dict(**rng)
    for test in rules[wf]:
        rk_in = rng_next[test["k"]]
        rng_yes = dict(**rng_next)
        if test["op"] == ">":
            rng_yes[test["k"]] = [max(test["v"] + 1, rk_in[0]), rk_in[1]]
            rng_next[test["k"]] = [rk_in[0], min(test["v"], rk_in[1])]
        else:
            rng_next[test["k"]] = [max(test["v"], rk_in[0]), rk_in[1]]
            rng_yes[test["k"]] = [rk_in[0], min(test["v"] - 1, rk_in[1])]

        if all(r[0]<=r[1] for r in rng_yes.values()):
            wf_yes = test["target"]
            if wf_yes == "A":
                prod = 1
                for v0, v1 in rng_yes.values():
                    prod *= v1 - v0 + 1
                total += prod
            elif wf_yes != "R":
                total += propagate(rng_yes, wf_yes)
    return total

print(propagate({"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}, "in"))
