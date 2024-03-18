import csv
from anytree import Node, RenderTree


with open("niveldescripcion_2023.csv", "r") as fniveldescripcion:
    data = csv.reader(fniveldescripcion, delimiter='|')
    levels_dict = { x[0]:x[1] for x in data }


find_root = False
root = None
node_dict = {}

with open("clasificacion_2023.csv", "r") as fclasificacion:
    data = csv.reader(fclasificacion, delimiter='|')
    for x in data:
        if x[0].startswith("A1"):

            if not find_root and bool(x[2]) == False:
                root = Node(f"{x[0]}-{x[1]} [{levels_dict.get(x[3])}({x[3]})]")
                find_root = True
                continue

            node = Node(f"{x[0]}-{x[1]} [{levels_dict.get(x[3])}({x[3]})]", parent=node_dict.get(x[2], root))
            node_dict[x[0]] = node
            

for pre, fill, node in RenderTree(root):
    print(f"{pre}{node.name}")