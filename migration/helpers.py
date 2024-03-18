import csv
from dataclasses import asdict
from atom_description_headers import HEADERS
from csv_parser import CSVDescription
from thefuzz import fuzz
from estado_fisico import physicalChars
from ingreso import origen_ingreso

def get_identifier(clasificacion: str):
    _, identifier = clasificacion.rsplit(".", 1)
    return identifier


def generate_csv_import_atom(objs_csv: "list[CSVDescription]", namefile="output.csv"):

    with open(namefile, mode="w", newline="") as archivo_csv:
        writer_csv = csv.DictWriter(archivo_csv, fieldnames=CSVDescription.__annotations__.keys())

        writer_csv.writeheader()

        for obj in objs_csv:
            writer_csv.writerow(asdict(obj))


def fill_csv_object_fields(csv_: CSVDescription, row):
                # ee
    csv_.identifier = row['numerodocumento'] if row['numerodocumento'] else get_identifier(row["clasificacion_ID"])
    csv_.extentAndMedium = row['volumen'] or '' # hh
    csv_.scopeAndContent = row['alcancecontenido'].replace("\n", "") if row['alcancecontenido'] else '' # ll
    csv_.relatedUnitsOfDescription = row['unidadesdescripcion'] or '' # yy

    # jj
    if row['historiaarchivist'] and row['historiainstbio']:
        csv_.archivalHistory = f"{row['historiaarchivist']} {row['historiainstbio']}"
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


def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False
    

def get_title_file(url):
    _, namefilewithext = url.rsplit("/", 1)
    namefile, _ = namefilewithext.split(".", 1)
    return namefile


"""
5339.0006   5339.0006: 5339/6 
5388.0001   5388.0003: 5388/1 - 5388/3
5388.0006   5388.0006: 5388/6
10.0018	    10.0018: 10/18
30.001      30.001: 30/10
30.0001     30.0001: 30/1
92672	6759.0017	6759.0017: 6759/17 -> 6759/170
"""


def _normalize_signature(sig):
    iCarpetaMaxima = 10000
    iIncMin = 0.000001

    box, envelop = str(sig).split(".")

    fenvelop = float(f"0.{envelop}")

    zeros = envelop.count("0")

    if zeros:
        envelop = int(round(fenvelop * iCarpetaMaxima))
    else:
        envelop = None
    
    if envelop is not None and envelop:
        return f"{box}/{envelop}"
    return f"{box}"


def get_signature(ini, fin):
    sig_ini = _normalize_signature(ini)
    sig_fin = _normalize_signature(fin)

    if sig_ini == sig_fin:
        return sig_ini
    else:
        return f"{sig_ini} - {sig_fin}"
    



def find_similarities(list_names, find_name, threshold=90):

    similarities = []

    for name in list_names:
        similarity = fuzz.ratio(name, find_name)
        if similarity >= threshold and name not in similarities:
            similarities.append(name)

    return similarities


def setvars_levels_description(lvl_, sublvl_):
    if lvl_ == 'A1':
        DIGITAL_OBJECT_LEAF_NAME = 'Unidad documental simple'
        PARENT_SLUG_FONDO = f"a1-{sublvl_}"
        LEVEL_ZERO = "A1"
        LEVEL_ONE = f"A1.{sublvl_}"
        SUBPARENTS_FOND = [4, 37]
        LEAF_LEVEL = 9
        OUTPUT_NAME_CSV = f"fondo_ugt_a1_{sublvl_}.csv"

    elif lvl_ == 'F1':
        DIGITAL_OBJECT_LEAF_NAME = 'Unidad Fotográfica'
        PARENT_SLUG_FONDO = f"f1-{sublvl_}"
        LEVEL_ZERO = "F1"
        LEVEL_ONE = f"F1.{sublvl_}"
        SUBPARENTS_FOND = [12]
        LEAF_LEVEL = 14
        OUTPUT_NAME_CSV = f"fondo_ugt_f1_{sublvl_}.csv"

    elif lvl_ == 'S1':
        DIGITAL_OBJECT_LEAF_NAME = 'Unidad Sonora'
        PARENT_SLUG_FONDO = f"s1-{sublvl_}"
        LEVEL_ZERO = "S1"
        LEVEL_ONE = f"S1.{sublvl_}"
        SUBPARENTS_FOND = [40] 
        LEAF_LEVEL = 41
        OUTPUT_NAME_CSV = f"fondo_ugt_s1_{sublvl_}.csv"

    elif lvl_ == 'M1':
        DIGITAL_OBJECT_LEAF_NAME = 'Unidad Gráfica'
        PARENT_SLUG_FONDO = f"m1-{sublvl_}"
        LEVEL_ZERO = "M1"
        LEVEL_ONE = f"M1.{sublvl_}"
        SUBPARENTS_FOND = [34] 
        LEAF_LEVEL = 35
        OUTPUT_NAME_CSV = f"fondo_ugt_m1_{sublvl_}.csv"  

    else:
        exit()
        
    return DIGITAL_OBJECT_LEAF_NAME,PARENT_SLUG_FONDO,LEVEL_ZERO,LEVEL_ONE,SUBPARENTS_FOND,LEAF_LEVEL,OUTPUT_NAME_CSV


def load_persons(BASE_PATH, persons_list):
    with open(BASE_PATH.parent / "personas" / "_persons_v3.csv", "r") as fpersons:
        data = csv.reader(fpersons, delimiter='|')
        for x in data:
            persons_list.append(x[1])


def load_levelsdescriptions(BASE_PATH):
    with open(BASE_PATH / "niveldescripcion_2023.csv", "r") as fniveldescripcion:
        data = csv.reader(fniveldescripcion, delimiter='|')
        levels_dict = { x[0]:x[1] for x in data }
    return levels_dict