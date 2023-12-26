import sys
from functools import cache

base = __file__.split("/")[-1].split(".")[0]
fn = f"{base}{'test' if 't' in sys.argv else 'input'}.txt"
with open(fn, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f.readlines()]

links = []
net = {}
start_node = None
for line in lines:
    node_in, nodes_out = line.split(": ")
    if not start_node:
        start_node = node_in
    for node_out in nodes_out.split(" "):
        links.append(tuple(sorted([node_in, node_out])))
        if node_in not in net:
            net[node_in] = set()
        if node_out not in net:
            net[node_out] = set()
        net[node_in].add(node_out)
        net[node_out].add(node_in)

total_nodes = len(net)
total_links = len(links)


def find_subnet_size(_start, skip_links):
    subnet, next_nodes = set([_start]), set([_start])
    while next_nodes:
        next_next_nodes = set()
        for nodea in next_nodes:
            for nodeb in net[nodea]:
                if nodeb not in subnet and tuple(sorted([nodea, nodeb])) not in skip_links:
                    next_next_nodes.add(nodeb)
        next_nodes = next_next_nodes
        subnet.update(next_nodes)
    return len(subnet)


@cache
def find_shortest_route_around(link):
    subnet, next_nodes = set([link[0]]), set([link[0]])
    steps = 0
    while next_nodes:
        steps += 1
        next_next_nodes = set()
        for nodea in next_nodes:
            for nodeb in net[nodea]:
                if nodeb not in subnet and tuple(sorted([nodea, nodeb])) != link:
                    if nodeb == link[1]:
                        return steps
                    next_next_nodes.add(nodeb)
        next_nodes = next_next_nodes
        subnet.update(next_nodes)
    return len(subnet)


def is_net_broken(skip_links):
    skip_list = list(skip_links)
    starter, tester = skip_list[0]
    l1a, l1b = skip_list[1]
    l2a, l2b = skip_list[2]
    subnet, next_nodes = set([starter]), set([starter])
    while next_nodes:
        next_next_nodes = set()
        for nodea in next_nodes:
            for nodeb in net[nodea]:
                if nodeb not in subnet and tuple(sorted([nodea, nodeb])) not in skip_links:
                    if nodeb == tester:
                        return False
                    if (nodeb == l1a and l1b in subnet) or (nodeb == l1b and l1a in subnet):
                        return False
                    if (nodeb == l2a and l2b in subnet) or (nodeb == l2b and l2a in subnet):
                        return False
                    next_next_nodes.add(nodeb)
        next_nodes = next_next_nodes
        subnet.update(next_nodes)
    return True


print(f"nodes: {total_nodes}, links: {total_links}")

# test first the links that take the longest to circumvent, if you remove a single link
# these are likely to be the best ones to remove (indeed, the first after sorting this way
# was one of the three to remove)
links.sort(key=lambda li: -find_shortest_route_around(li))

for i in range(total_links - 2):
    print(f"link {i} - shortest alternate: {find_shortest_route_around(links[i])}")
    for j in range(i + 1, total_links - 1):
        for k in range(j + 1, total_links):
            skip_links = set([links[i], links[j], links[k]])
            if is_net_broken(skip_links):
                sns = find_subnet_size(start_node, skip_links)
                print(f"Found separate subnets, sizes {sns} and {total_nodes - sns}, product: {sns * (total_nodes - sns)}")
                sys.exit()
