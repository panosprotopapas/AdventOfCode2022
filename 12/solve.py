from py2neo import *

n4j = Graph(f"bolt://0.0.0.0:7687", auth=("neo4j", "test"))
match = NodeMatcher(n4j)
path = Relationship.type("PATH")


def allowed_location(i, j):
    if i in range(41) and j in range(167):
        return True
    return False


def locations_to_check(i, j):
    return [
        (i - 1, j),
        (i, j - 1),
        (i + 1, j),
        (i, j + 1),
    ]


def reachable_locations(this_loc, other_loc, heights):
    if heights[this_loc[0]][this_loc[1]] + 1 >= heights[other_loc[0]][other_loc[1]]:
        return True
    return False


# Replace S->@ and E->{, make all chars into ascii values and subtract 64
with open("input.txt", encoding="utf-8") as f:
    heights = [
        list(map(ord, list(line.replace("S", "`").replace("E", "{").strip())))
        for line in f.readlines()
    ]

heights = [[number - 96 for number in row] for row in heights]

with open("output.txt", "w") as f:
    for row in heights:
        string = ""
        for number in row:
            string += str(number)
        f.write(string + "\n")


nodes = list()
for i, current_row in enumerate(heights):
    for j, height in enumerate(current_row):
        if height == 0:
            nodes.append(Node("START", row=i, col=j, height=1))
            heights[i][j] = 1
        elif height == 27:
            nodes.append(Node("END", row=i, col=j, height=26))
            heights[i][j] = 26
        else:
            nodes.append(Node(row=i, col=j, height=height))

node_subgraph = nodes.pop()
for node in nodes:
    node_subgraph = node_subgraph | node
n4j.create(node_subgraph)

edges = list()
for i, current_row in enumerate(heights):
    for j, height in enumerate(current_row):
        nearby_locs = [
            l for l in locations_to_check(i, j) if allowed_location(l[0], l[1])
        ]
        reachable_locs = [l for l in nearby_locs if height + 1 >= heights[l[0]][l[1]]]
        edges.extend([[(i, j), (l[0], l[1])] for l in reachable_locs])

for edge in edges:
    cypher = (
        f"""MATCH (a) WHERE a.row={edge[0][0]} AND a.col={edge[0][1]} """
        f"""MATCH (b) WHERE b.row={edge[1][0]} AND b.col={edge[1][1]} """
        f"""CREATE (a)-[:PATH]->(b)"""
    )
    n4j.run(cypher)

# Part 1
cypher = "MATCH (a:START), (b:END), p = shortestPath((a)-[:PATH*]->(b)) RETURN length(p)"
res = n4j.run(cypher).data()
print(res[0]["length(p)"])


# Part 2
cypher = "MATCH (a), (b:END), p = shortestPath((a)-[:PATH*]->(b)) WHERE a.height=1 RETURN length(p)"
res = n4j.run(cypher).data()
sps = [spath['length(p)'] for spath in res]
print(min(sps))
