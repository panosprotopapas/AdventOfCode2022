from collections import namedtuple
from py2neo import *
from itertools import *

n4j = Graph(f"bolt://0.0.0.0:7687", auth=("neo4j", "test"))
match = NodeMatcher(n4j)
path = Relationship.type("PATH")

##########
# PART 1 #
##########

# Valve class
Valve = namedtuple("Valve", "name flow links")

# Get all valves
temp = [
    l.replace("Valve ", "")
    .replace(" has flow rate=", ";")
    .replace(" tunnel leads to valve ", "")
    .replace(" tunnels lead to valves ", "")
    .replace(", ", ";")
    .split(";")
    for l in open("16/input.txt", encoding="utf-8").read().split("\n")
]
valves = {
    i[0].lower(): Valve(
        name=i[0].lower(), flow=int(i[1]), links=[lead.lower() for lead in i[2:]]
    )
    for i in temp
}

# Create nodes and edges
nodes = dict()
for valve, info in valves.items():
    if info.flow == 0 and valve != "aa":
        nodes[valve] = Node("Zero_Flow", name=info.name, flow=info.flow)
    elif valve == "aa":
        nodes[valve] = Node("Starting_Point", name=info.name, flow=info.flow)
    else:
        nodes[valve] = Node("Non_Zero_Flow", name=info.name, flow=info.flow)
edges = list()
for _, info in valves.items():
    for link in info.links:
        edges.append(Relationship(nodes[info.name], "Leads_to", nodes[link]))

# # Import in Neo4j
# sg = Subgraph(nodes=nodes.values(), relationships=edges)
# n4j.create(sg)


def shortest_path(node_1, node_2):
    cypher = f"""MATCH (p1 {{ name: "{node_1}" }}),(p2 {{ name: "{node_2}" }}), path = shortestPath((p1)-[*]->(p2)) RETURN length(path) as result"""
    return n4j.run(cypher).data()[0]["result"]


# Create non-zero + aa
useful_valves = {k: v for k, v in valves.items() if v.flow > 0 or v.name == "aa"}

# Create distance-dictionary of paths
distances = {valve: dict() for valve in useful_valves}
valves_list = list(useful_valves)
for _ in range(len(valves_list) - 1):
    valve = valves_list[0]
    valves_list = valves_list[1:]
    for other_valve in valves_list:
        d = shortest_path(valve, other_valve)
        distances[valve][other_valve] = d
        distances[other_valve][valve] = d

# Check pressure of all permutations, after removing aa. The best path with 7 hops takes
# long enough to not allow more hops in 30 mins. So best out of 7 is best.
useful_valves.pop("aa")
max_pressure = 0
best_path = None
counter = 0

for i in permutations(useful_valves, 7):
    counter += 1
    t = 30
    pressure = 0
    t -= 1 + distances["aa"][i[0]]
    pressure += useful_valves[i[0]].flow * t
    for index, j in enumerate(i[:-1]):
        t -= 1 + distances[j][i[index + 1]]
        pressure += useful_valves[i[index + 1]].flow * t
        if pressure > max_pressure:
            max_pressure = pressure
            best_path = i

print(f"Part 1:\nBest path:{best_path}\nMax Pressure:{max_pressure}\n")


# By looking at the graph in Neo4j (and a little trial and error), it makes sense that elephant and person
# will obviously take quite different paths. So remove points from elephant that belong to the "other" path.
# This makes things way faster, and also after checking solutions, no more than 6 valves can be opened.
# Obviously this is input specific!
useful_valves = {k: v for k, v in valves.items() if v.flow > 0}
max_pressure = 0
best_path = None
counter = 0
useful_valves.pop("ek")
useful_valves.pop("fx")
useful_valves.pop("vw")
useful_valves.pop("tq")
useful_valves.pop("eg")
useful_valves.pop("kr")

for i in permutations(useful_valves, 6):
    counter += 1
    t = 26
    pressure = 0
    t -= 1 + distances["aa"][i[0]]
    pressure += useful_valves[i[0]].flow * t
    for index, j in enumerate(i[:-1]):
        t -= 1 + distances[j][i[index + 1]]
        pressure += useful_valves[i[index + 1]].flow * t
        if pressure > max_pressure:
            max_pressure = pressure
            best_path = i

print(f"Part 2:\nBest path 1:{best_path}\nMax Pressure 1:{max_pressure}")
total = max_pressure

# Similarly, remove valves from other possible paths
useful_valves = {k: v for k, v in valves.items() if v.flow > 0}
max_pressure = 0
best_path = None
counter = 0
useful_valves.pop("uw")
useful_valves.pop("tg")
useful_valves.pop("ks")
useful_valves.pop("fg")
useful_valves.pop("ap")
useful_valves.pop("wy")

for i in permutations(useful_valves, 6):
    counter += 1
    t = 26
    pressure = 0
    t -= 1 + distances["aa"][i[0]]
    pressure += useful_valves[i[0]].flow * t
    for index, j in enumerate(i[:-1]):
        t -= 1 + distances[j][i[index + 1]]
        pressure += useful_valves[i[index + 1]].flow * t
        if pressure > max_pressure:
            max_pressure = pressure
            best_path = i

print(
    f"Best path 2:{best_path}\nMax Pressure 2:{max_pressure}\nTotal: {max_pressure + total}"
)
