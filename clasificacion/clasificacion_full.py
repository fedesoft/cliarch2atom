import csv
from anytree import Node, RenderTree
import pymssql
import uuid

q_get_archivo_by_clas_and_level = """SELECT ID, numerodocumento, titulo FROM archivo.dbo.archivo 
                                    WHERE clasificacion_ID LIKE '{clas}' 
                                    AND niveldescripcion_ID = {level};"""

q_recurso = """SELECT * FROM archivo.dbo.recurso WHERE archivo_ID = ${archivo_id}"""


conn = pymssql.connect("localhost", "SA", "<change-password>", "archivo")
cursor = conn.cursor(as_dict=True)

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
                root = Node((x[0], x[1], levels_dict.get(x[3]), int(x[3])))
                find_root = True
                continue

            node = Node((x[0], x[1].strip(), levels_dict.get(x[3]), int(x[3])), parent=node_dict.get(x[2], root))
            node_dict[x[0]] = node

            if x[0].startswith("A1.09"):
        
                query = q_get_archivo_by_clas_and_level.format(
                    clas=x[0],
                    level=9)
                
                cursor.execute(query)
                row = cursor.fetchall()

                if row:
                    for obj in row:
                        # print(obj)
                        new_node = Node((str(obj['ID']), obj['numerodocumento'], levels_dict.get('9'), 9), parent=node)

                        query = q_recurso.format(archivo_id=obj['ID'])
                        cursor.execute(query)
                        row_objects_digital = cursor.fetchall()

                        if row_objects_digital:
                            for obj_digital in row_objects_digital:
                                Node((uuid.uuid4().hex, obj_digital['url'], 'File', 90), parent=new_node)

            if x[0].startswith("A1.11"):
                break
    


for pre, fill, node in RenderTree(root):
    print(f"{pre}{node.name}")

conn.close()