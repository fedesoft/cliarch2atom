import os
import csv
from anytree import Node, RenderTree
import pymssql
import uuid
import subprocess

from raw_queries import (q_get_archivo_by_clas_and_level, q_recurso, q_recurso_no_order)

PATH_DOCUMENTS = "/media/desarrollo/WD/_ARCHIVO"

def get_size_file(url):
    try:
        size = os.path.getsize(url)
        return size / (1024 * 1024)
    except FileNotFoundError:
        return 0
    
def join_pdfs(pdfs, ruta_destino):
    # archivos_pdf = [archivo for archivo in os.listdir(ruta_origen) if archivo.endswith(".pdf") and archivo.startswith(prefijo)]

    # Ordenar la lista de archivos para asegurar el orden correcto
    # archivos_pdf.sort()

    # Construir la lista de rutas completas a los archivos PDF
    # rutas_completas = [os.path.join(ruta_origen, archivo) for archivo in archivos_pdf]

    # Comando pdfunite para unir archivos PDF
    comando = ["pdfunite"] + pdfs + [ruta_destino]

    # Ejecutar el comando utilizando subprocess
    subprocess.run(comando) 


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

            node = Node((x[0], x[1], levels_dict.get(x[3]), int(x[3])), parent=node_dict.get(x[2], root))
            node_dict[x[0]] = node


            if x[0].startswith("A1.09"):
                
                # search unidades documentales
                query = q_get_archivo_by_clas_and_level.format(
                    clas=x[0],
                    level=9)
                
                cursor.execute(query)
                row = cursor.fetchall()

                if row:
                    for obj in row:
                        new_node = Node((str(obj['ID']), obj['titulo'], obj['numerodocumento'], levels_dict.get('9'), 9), parent=node)

                        try: 
                            query = q_recurso.format(archivo_id=obj['ID'])
                            cursor.execute(query)
                            row_objects_digital = cursor.fetchall()
                        except:
                            query = q_recurso_no_order.format(archivo_id=obj['ID'])
                            cursor.execute(query)
                            row_objects_digital = cursor.fetchall()

                        # if row_objects_digital and obj['clasificacion_ID'].startswith('A1.09.01.01'):
                        #     for obj_digital in row_objects_digital:
                        #         Node((f"${uuid.uuid4().hex}", f"/tmp{obj_digital['url']}", 'Unidad documental simple', 90), parent=new_node)


                        if row_objects_digital and obj['clasificacion_ID'].startswith('A1.09'):
                            amount_size = 0
                            files_pdf = []

                            for e, obj_digital in enumerate(row_objects_digital):

                                size = get_size_file(f"{PATH_DOCUMENTS}{obj_digital['url']}")
                                files_pdf.append(f"{PATH_DOCUMENTS}{obj_digital['url']}")
                                amount_size += size

                                path_destination, namefilewithext = obj_digital['url'].rsplit("/", 1)
                                Node((f"${uuid.uuid4().hex[:8]}", namefilewithext, 'File', f"{round(size, 2)} MB"), parent=new_node)
                                # if e == 1:
                                #     break
                            
                            Node((f"${uuid.uuid4().hex[:8]}", 'Total size', '', f"{round(amount_size, 2)} MB"), parent=new_node)
                                # Node((f"${uuid.uuid4().hex}", f"/tmp{obj_digital['url']}", 'Unidad documental simple', 90), parent=new_node)
                                # if e == 1:
                                #     break
                            join_pdfs(files_pdf, path_destination)


conn.close()


START_LEVEL = "A1.09"

for pre, fill, node in RenderTree(root):
    if (node.name[0]).startswith(START_LEVEL) or (node.name[0]).isdigit() or node.name[0].startswith("$"):
        print(f"{pre}{node.name}")
