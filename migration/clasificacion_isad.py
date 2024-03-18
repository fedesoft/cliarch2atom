import sys
from copy import copy
import csv
from datetime import datetime
from anytree import Node, RenderTree
from csv_parser import CSVDescription
import pymssql
import uuid    
import logging

from pathlib import Path

from raw_queries import (q_fechas, q_archivo, q_productor, q_lugar, q_materia, q_fechas_descripcion, 
                         q_get_archivo_by_clas_and_level, q_recurso, q_recurso_no_order, 
                         q_rango_signaturas, q_personas, q_entidades)

from helpers import (generate_csv_import_atom, get_identifier, 
                     fill_csv_object_fields, is_hex, get_title_file, 
                     get_signature, find_similarities, setvars_levels_description,
                     load_persons, load_levelsdescriptions)

logger = logging.getLogger('fudepa - isad')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


LEN_ARGV = len(sys.argv)

BASE_PATH = Path(__file__).parent

ARCHIVAL_INTITUTION = "Archivo de UGT Andalucía"


if LEN_ARGV == 4:

    lvl_ = sys.argv[1]
    sublvl_ = sys.argv[2]
    digital_objects_test = sys.argv[3]

    DIGITAL_OBJECT_LEAF_NAME, PARENT_SLUG_FONDO, LEVEL_ZERO, LEVEL_ONE, SUBPARENTS_FOND, LEAF_LEVEL, OUTPUT_NAME_CSV = setvars_levels_description(lvl_, sublvl_)  

else:
    exit()


logger.info("Loading persons...")
persons_list = []
load_persons(BASE_PATH, persons_list)
persons_list = persons_list[1:]

logger.info("Loading levels of descriptions...")
levels_dict = load_levelsdescriptions(BASE_PATH)

logger.info("Connect database...")
conn = pymssql.connect("localhost", "SA", "<change-password>", "archivo")
cursor = conn.cursor(as_dict=True)

if bool(int(digital_objects_test)):
    logger.info("Digital objects en modo TEST...")

find_root = False
root = None
node_dict = {}

with open(BASE_PATH / "clasificacion_2023.csv", "r") as fclasificacion:
    data = csv.reader(fclasificacion, delimiter='|')
    for x in data:
        if x[0].startswith(LEVEL_ZERO):

            if not find_root and bool(x[2]) == False:
                root = Node((x[0], x[1], levels_dict.get(x[3]), int(x[3])))
                find_root = True
                continue

            node = Node((x[0], x[1], levels_dict.get(x[3]), int(x[3])), parent=node_dict.get(x[2], root))
            node_dict[x[0]] = node


            if x[0].startswith(LEVEL_ONE):
                
                # search unidades documentales
                query = q_get_archivo_by_clas_and_level.format(
                    clas=x[0],
                    level=LEAF_LEVEL)
                
                cursor.execute(query)
                row = cursor.fetchall()

                if row:

                    for obj in row:

                        # if obj['numerodocumento'].startswith("ADUGT"):
                        # if "UGT" in obj['numerodocumento']:
                        # print(obj)
                        if obj['numerodocumento']:

                            try: 
                                query = q_recurso.format(archivo_id=obj['ID'])
                                cursor.execute(query)
                                row_objects_digital = cursor.fetchall()
                            except:
                                query = q_recurso_no_order.format(archivo_id=obj['ID'])
                                cursor.execute(query)
                                row_objects_digital = cursor.fetchall()


                            if row_objects_digital and len(row_objects_digital) == 1:
                                new_node = Node((str(obj['ID']), obj['numerodocumento'], levels_dict.get(str(LEAF_LEVEL)), LEAF_LEVEL, f'/backup{row_objects_digital[0]["url"]}'), parent=node)
                                continue
                                
                            new_node = Node((str(obj['ID']), obj['numerodocumento'], levels_dict.get(str(LEAF_LEVEL)), LEAF_LEVEL, ''), parent=node)

                            if row_objects_digital: # and obj['clasificacion_ID'].startswith('A1.01.01'):
                                for e, obj_digital in enumerate(row_objects_digital):
                                    Node((f"${uuid.uuid4().hex}", f'/backup{obj_digital["url"]}', DIGITAL_OBJECT_LEAF_NAME, 90), parent=new_node)
                                    if bool(int(digital_objects_test)) and e == 0: break

                    

index = 500
idx_dict = dict()

START_LEVEL = LEVEL_ONE

# Copy of tree: search parents and set indexes
for pre, fill, node in RenderTree(root):
    if (node.name[0]).startswith(START_LEVEL) or (node.name[0]).isdigit() or node.name[0].startswith("$"):
        idx_dict.update({node.name[0]: index})
        index += 1


objs_csv_list = []
index = 500

for pre, fill, node in RenderTree(root):
    if (node.name[0]).startswith(START_LEVEL):

        level = node.name[3]
        
        csv_ = CSVDescription()
        csv_.legacyId = index

        if level in SUBPARENTS_FOND:
            csv_.qubitParentSlug = PARENT_SLUG_FONDO
        else:
            # node.parent
            csv_.parentId = idx_dict.get(node.parent.name[0])
        
        csv_.title = node.name[1]
        csv_.identifier = get_identifier(node.name[0])
        csv_.levelOfDescription = node.name[2]
        csv_.repository = ARCHIVAL_INTITUTION # ii

        csv_.xClasificacion = node.name[0]
        csv_.xLevel = node.name[3]
        
        query = q_get_archivo_by_clas_and_level.format(
            clas=node.name[0],
            level=node.name[3])
        
        # print(node.name[0])
        
        cursor.execute(query)
        row = cursor.fetchone()
        csv_.xIDMSSQL = row and row['ID']

        if row:
            obj = copy(row)

            fill_csv_object_fields(csv_, row)

            ## LUGARES
            query = q_lugar.format(archivo_id=obj['ID'])
            cursor.execute(query)
            row = cursor.fetchall()

            # aae
            csv_.placeAccessPoints = "|".join([ x['nombre'] for x in row])

            # bbb eventActors van separados por |
            # csv_.eventActors = row

            ## MATERIA
            query = q_materia.format(archivo_id=obj['ID'])
            cursor.execute(query)
            row = cursor.fetchall()

            # aad
            csv_.subjectAccessPoints = "|".join([ x['nombre'] for x in row])

            ## FECHAS

            query = q_fechas.format(archivo_id=obj['ID'])
            cursor.execute(query)
            row = cursor.fetchall()

            # print("FECHAS", row)

            dates_formated_list = []

            for x in row:

                fecha_ini_: datetime = x['fechaIni']
                fecha_fin_: datetime = x['fechaFin']

                if x['tipoIni'] == 0: # completa
                    res = f"{fecha_ini_.strftime('%Y/%m/%d')}-{fecha_fin_.strftime('%Y/%m/%d')}"
                elif x['tipoIni'] == 1: # año y mes
                    res = f"{fecha_ini_.strftime('%Y/%m')}-{fecha_fin_.strftime('%Y/%m')}"
                elif x['tipoIni'] == 2: # año
                    res = f"{fecha_ini_.strftime('%Y')}-{fecha_fin_.strftime('%Y')}"
                
                dates_formated_list.append(res)
            
            csv_.eventDates = "|".join(dates_formated_list)


            ## FECHAS DESCRIPCIÓN

            query = q_fechas_descripcion.format(archivo_id=obj['ID'])
            cursor.execute(query)
            row = cursor.fetchall()

            # print("FECHAS DESCRIPCIÓN", row)

            dates_formated_list = []

            for x in row:

                fecha_ini_: datetime = x['fechaIni']
                fecha_fin_: datetime = x['fechaFin']

                if x['tipoIni'] == 0: # completa
                    res = f"{fecha_ini_.strftime('%Y/%m/%d')}"
                elif x['tipoIni'] == 1: # año y mes
                    res = f"{fecha_ini_.strftime('%Y/%m')}"
                elif x['tipoIni'] == 2: # año
                    res = f"{fecha_ini_.strftime('%Y')}"
                
                dates_formated_list.append(res)
            
            csv_.revisionHistory = "\n".join(dates_formated_list)   

        objs_csv_list.append(csv_)
        index += 1

    if (node.name[0]).isdigit(): # level LEAF

        level = node.name[3]
        csv_ = CSVDescription()
        csv_.legacyId = index
        csv_.parentId = idx_dict.get(node.parent.name[0]) 

        csv_.identifier = node.name[1].strip()
        csv_.levelOfDescription = node.name[2]
        csv_.repository = ARCHIVAL_INTITUTION # ii   

        csv_.xClasificacion = ''
        csv_.xLevel = level

        if node.name[4]:
            csv_.digitalObjectPath = node.name[4]  

        query = q_archivo.format(archivo_id=node.name[0])
                
        cursor.execute(query)
        row = cursor.fetchone()
        csv_.xIDMSSQL = row and row['ID']

        if row:
            obj = copy(row)

            csv_.title = row['titulo']

            fill_csv_object_fields(csv_, row)

            ## LUGARES
            query = q_lugar.format(archivo_id=obj['ID'])
            cursor.execute(query)
            row = cursor.fetchall()

            # aae
            csv_.placeAccessPoints = "|".join([ x['nombre'] for x in row])

            # bbb eventActors van separados por |
            # csv_.eventActors = row

            ## MATERIA
            query = q_materia.format(archivo_id=obj['ID'])
            cursor.execute(query)
            row = cursor.fetchall()

            # aad
            csv_.subjectAccessPoints = "|".join([ x['nombre'] for x in row])

            ## FECHAS

            query = q_fechas.format(archivo_id=obj['ID'])
            cursor.execute(query)
            row = cursor.fetchall()

            # print("FECHAS", row)

            dates_formated_list = []

            for x in row:

                fecha_ini_: datetime = x['fechaIni']
                fecha_fin_: datetime = x['fechaFin']

                if x['tipoIni'] == 0: # completa
                    res = f"{fecha_ini_.strftime('%Y/%m/%d')}-{fecha_fin_.strftime('%Y/%m/%d')}"
                elif x['tipoIni'] == 1: # año y mes
                    res = f"{fecha_ini_.strftime('%Y/%m')}-{fecha_fin_.strftime('%Y/%m')}"
                elif x['tipoIni'] == 2: # año
                    res = f"{fecha_ini_.strftime('%Y')}-{fecha_fin_.strftime('%Y')}"
                
                dates_formated_list.append(res)
            
            csv_.eventDates = "|".join(dates_formated_list)


            ## FECHAS DESCRIPCIÓN

            query = q_fechas_descripcion.format(archivo_id=obj['ID'])
            cursor.execute(query)
            row = cursor.fetchall()

            # print("FECHAS DESCRIPCIÓN", row)

            dates_formated_list = []

            for x in row:

                fecha_ini_: datetime = x['fechaIni']
                fecha_fin_: datetime = x['fechaFin']

                if x['tipoIni'] == 0: # completa
                    res = f"{fecha_ini_.strftime('%Y/%m/%d')}"
                elif x['tipoIni'] == 1: # año y mes
                    res = f"{fecha_ini_.strftime('%Y/%m')}"
                elif x['tipoIni'] == 2: # año
                    res = f"{fecha_ini_.strftime('%Y')}"
                
                dates_formated_list.append(res)
            
            csv_.revisionHistory = "\n".join(dates_formated_list) 

            # CAJAS
            query = q_rango_signaturas.format(archivo_id=obj['ID'])
            cursor.execute(query)
            row = cursor.fetchall()  

            signatures_formated_list = []

            for x in row:
                # print(obj['ID'])
                signatures_formated_list.append(get_signature(x['signaturaIni'], x['signaturaFin']))

            csv_.physicalObjectName = "|".join(signatures_formated_list)
            if csv_.physicalObjectName:
                csv_.physicalObjectLocation = sys.argv[1] # A1
                csv_.physicalObjectType = "Caja"

            # PRODUCTOR, PERSON AND INSTITUTIONS

            actors_list = [] 
            types_list = []

            ## PRODUCTOR
            query = q_productor.format(archivo_id=obj['ID'])
            cursor.execute(query)
            row = cursor.fetchall() 

            for x in row:
                actors_list.append(x['nombre'])
                types_list.append('NULL')
            
            ## PERSONS

            query = q_personas.format(archivo_id=obj['ID'])
            cursor.execute(query)
            row = cursor.fetchall() 

            for x in row:

                nombre_ = x['nombre']

                if x['nombre'] in persons_list:
                    nombre_ = x['nombre']
                
                else:
                    similarities_ = find_similarities(persons_list, nombre_)
                    if similarities_:
                        nombre_ = similarities_[-1]
                    else:
                        if "." in nombre_:
                            nombre_ = nombre_.split(".")[0]
                        similarities_ = find_similarities(persons_list, nombre_, 85)
                        if similarities_:
                            print(nombre_, " => ", similarities_[-1])
                            nombre_ = similarities_[-1]
                        else:      
                            print(">>> NO ENCONTRADA SIMILITUD PARA: ", nombre_)
                            nombre_ = x['nombre']


                actors_list.append(nombre_)
                types_list.append('Documentos relacionados')

            ## INSTITUTIONS

            query = q_entidades.format(archivo_id=obj['ID'])
            cursor.execute(query)
            row = cursor.fetchall() 

            for x in row:
                actors_list.append(x['nombre'])
                types_list.append('Documentos relacionados')

            csv_.eventActors = "|".join(actors_list)
            csv_.eventTypes = "|".join(types_list)            

        objs_csv_list.append(csv_)
        index += 1
        
    if node.name[0].startswith("$"):

        level = node.name[3]
        csv_ = CSVDescription()
        csv_.legacyId = index
        # print(node)
        csv_.parentId = idx_dict.get(node.parent.name[0]) 

        # csv_.identifier = node.name[1].strip()
        csv_.levelOfDescription = node.name[2]
        csv_.repository = ARCHIVAL_INTITUTION # ii   

        csv_.xClasificacion = ''
        csv_.xLevel = level 

        csv_.digitalObjectPath = node.name[1]  

        csv_.title = get_title_file(node.name[1])     

        objs_csv_list.append(csv_)
        index += 1


conn.close()

generate_csv_import_atom(objs_csv_list, namefile=OUTPUT_NAME_CSV)
