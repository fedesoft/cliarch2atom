import csv
from anytree import Node, RenderTree


with open("niveldescripcion_2023.csv", "r") as fniveldescripcion:
    data = csv.reader(fniveldescripcion, delimiter='|')
    levels_dict = { x[0]:x[0] for x in data }



root = Node(f"{levels_dict.get('1')}")
node_dict = {}

with open("relacionniveldescripcion_2023.csv", "r") as frelationlevels:
    data = csv.reader(frelationlevels, delimiter='|')
    for x in data:
        node = Node(f"{levels_dict.get(x[1])}", parent=node_dict.get(x[0], root))
        node_dict[x[1]] = node
            
for pre, fill, node in RenderTree(root):
    print(f"{pre}{node.name}")