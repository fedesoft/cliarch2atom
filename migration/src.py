from datetime import datetime
import pymssql

from raw_queries import (q_clasificacion, q_fechas, q_archivo, 
                         q_productor, q_lugar, q_materia, q_fechas_descripcion)
from csv_parser import CSVDescription
from niveles import levels_of_descriptions
from estado_fisico import physicalChars
from ingreso import origen_ingreso
from slugify import slugify

from helpers import generate_csv_import_atom, get_identifier

PARENT_SLUG_FONDO = "ugt-andalucia"

conn = pymssql.connect("localhost", "SA", "<change-password>", "archivo")
cursor = conn.cursor(as_dict=True)

query = q_clasificacion.format(clasificacion_id="A1.09.01%")
cursor.execute(query)

list_clasificacion = []

for row in cursor:
    # print("ID=%d, Name=%s" % (row['id'], row['name']))
    list_clasificacion.append(row)

objs_csv_list = []
root = None
parent = None
level = None
path = []

for e, obj in enumerate(list_clasificacion, 501):

    csv_ = CSVDescription()
    csv_.legacyId = e

    # El fondo raíz debe estar creado manualmente en ATOM
    if obj.get("niveldescripcion_ID") in [4, 37]:
        csv_.qubitParentSlug = PARENT_SLUG_FONDO
        root = csv_.legacyId
        parent = csv_.legacyId
        level = obj.get("niveldescripcion_ID")

    # elif level != obj.get("niveldescripcion_ID") and level < obj.get("niveldescripcion_ID"):
    #     level = obj.get("niveldescripcion_ID")
    #     parent = csv_.legacyId - 1
    #     csv_.parentId = parent

    # elif level != obj.get("niveldescripcion_ID") and level > obj.get("niveldescripcion_ID"):
    #     pass
    
    # else:
    #     csv_.parentId = parent
    

    query = q_archivo.format(archivo_id=obj['ID'])
    cursor.execute(query)
    row = cursor.fetchone()

    # print("---------------")
    # print(row)

    csv_.title = row["titulo"] # ff
    csv_.levelOfDescription = levels_of_descriptions.get(row["niveldescripcion_ID"]) # type: ignore # gg
    csv_.repository = "Archivo Histórico de UGT Andalucía" # ii
    
    
    '''
    Los niveles superiores no tienen numerodocumento, se organizar por el último número de su clasificación
        A1.09 UGT Andalucía 
        |
        |_ A1.09.01 Congresos (01)
            |_ A1.09.01.01 Congresos Ordinarios (01)
            |            |_ V congreso ... (ya tienen numerodocumento)
            |            |_ VI congreso ... ...
            |
            |_ A1.09.01.02 Congresos Extraordinarios (02)
    '''

    # ee
    csv_.identifier = row['numerodocumento'] if row['numerodocumento'] else get_identifier(row["clasificacion_ID"])
    csv_.extentAndMedium = row['volumen'] or '' # hh
    csv_.scopeAndContent = row['alcancecontenido'] or '' # ll
    csv_.relatedUnitsOfDescription = row['unidadesdescripcion'] or '' # yy

    # jj
    if row['historiaarchivist'] and row['historiainstbio']:
        csv_.archivalHistory = f"{row['historiaarchivist']}\n{row['historiainstbio']}"
    elif row['historiaarchivist'] and not row['historiainstbio']:
        csv_.archivalHistory = row['historiaarchivist']
    elif not row['historiaarchivist'] and row['historiainstbio']:
        csv_.archivalHistory = row['historiainstbio']

    # kk
    csv_.acquisition = origen_ingreso.get(row['ingreso_ID'], '')

    # uu
    if row['caracteristicasfisicas']:
        csv_.physicalCharacteristics = row['caracteristicasfisicas'] + ' ' + physicalChars.get(row['estadofisico_ID'], '')
    else:
        csv_.physicalCharacteristics = physicalChars.get(row['estadofisico_ID'], '')

    csv_.findingAids = row['instrumentosdescripcion'] or '' # vv
    csv_.appraisal = row['valoracion'] or '' # mm
    csv_.accruals = row['nuevosingresos'] or '' # nn
    csv_.accessConditions = row['condicionesacceso'] or '' # pp
    csv_.reproductionConditions = row['condicionesreproduccion'] or '' # qq

    csv_.locationOfOriginals = row['originales'] or '' # ww
    csv_.locationOfCopies = row['copias'] or '' # xx

    csv_.publicationNote = row['notapublicaciones'] or '' # zz
    csv_.generalNote = row['notas'] or '' # aac
    csv_.archivistNote = row['notaarchivero'] or '' # aaq

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

    print("FECHAS DESCRIPCIÓN", row)

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

    # print(">>>",csv_)

    objs_csv_list.append(csv_)

    generate_csv_import_atom(objs_csv_list)


conn.close()

