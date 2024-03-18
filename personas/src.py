import csv
from dataclasses import asdict
from csv_parser import CSVAuthorityRecord

objs_csv_list = []

def generate_csv_import_atom(objs_csv: "list[CSVAuthorityRecord]", namefile="output.csv"):

    with open(namefile, mode="w", newline="") as archivo_csv:
        writer_csv = csv.DictWriter(archivo_csv, fieldnames=CSVAuthorityRecord.__annotations__.keys())

        writer_csv.writeheader()

        for obj in objs_csv:
            writer_csv.writerow(asdict(obj))

with open("_persons_v3.csv", "r") as fpersons:
    data = csv.reader(fpersons, delimiter='|')
    for x in data:
        if x[0].isdigit():
            csv_ = CSVAuthorityRecord()
            csv_.typeOfEntity = "Persona"
            csv_.authorizedFormOfName = x[1]
            csv_.history = x[2]
            csv_.xIDMSSQL = x[0]

            objs_csv_list.append(csv_)

generate_csv_import_atom(objs_csv_list)