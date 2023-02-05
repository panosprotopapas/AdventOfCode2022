from treelib import Node, Tree

with open("07/input.txt") as f:
    commands = [l.strip().split(" ") for l in f]


class Object(object):
    def __init__(self, type, size=0):
        self.type = type
        self.size = size


tree = Tree()
tree.create_node("Root", "root", data=Object(type="folder"))
current_node = "root"
for c in commands:
    if c[0] == "$":
        if c[1] == "cd" and c[2] not in ["/"]:
            if c[2] == "..":
                current_node = ".".join(current_node.split(".")[:-1])
            else:
                new_current_node = f"{current_node}.{c[2]}"
                tree.create_node(
                    new_current_node,
                    new_current_node,
                    parent=current_node,
                    data=Object(type="folder"),
                )
                current_node = new_current_node
    elif c[0] != "dir":
        filename = f"{current_node}.{c[1]}"
        tree.create_node(
            filename,
            filename,
            parent=current_node,
            data=Object(type="file", size=int(c[0])),
        )

# Part 1
part_1 = 0
for node in tree.all_nodes_itr():
    if node.data.type == "folder":
        sub_tree = tree.subtree(node.identifier)
        folder_size = sum([int(node.data.size) for node in sub_tree.all_nodes_itr()])
        if folder_size < 100001:
            part_1 += folder_size
print(f"Part 1: {part_1}")

# Part 2
needed_space = 30000000 - (
    70000000 - sum([int(node.data.size) for node in tree.all_nodes_itr()])
)
part_2 = 70000000
for node in tree.all_nodes_itr():
    if node.data.type == "folder":
        sub_tree = tree.subtree(node.identifier)
        folder_size = sum([int(node.data.size) for node in sub_tree.all_nodes_itr()])
        if needed_space <= folder_size < part_2:
            part_2 = folder_size
print(f"Part 2: {part_2}")
