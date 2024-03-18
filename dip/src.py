import csv
import re
import metsrw

from metsrw import FSEntry, METSDocument

PATTERN = r"\b[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}\b"

mets = metsrw.METSDocument()

mets_ : METSDocument  = mets.fromfile("METS.03a731f2-3d5b-4152-a19b-7266297eab28.xml")

all_dip_files: "list[FSEntry]" = mets_._get_all_files_list()

print(mets_._root_elements[0].label)

uuids_and_filenames = dict()
with open("dip_objects_files.txt", "r") as fin:
    for x in fin.readlines():
        _, filename = x.rsplit("/", 1)
        uuid_ = re.search(PATTERN, filename)
        if uuid_:
            uuids_and_filenames.update({
                uuid_.group(): filename.strip()
            })

data_csv = []
for x in all_dip_files:
    if x.file_uuid in uuids_and_filenames.keys():
        data_csv.append((uuids_and_filenames[x.file_uuid], '', x.path))
        # print(f"{x.get_path()} | {x.file_uuid} | {x.mets_div_type} | {x.path}\n\n")


nombre_archivo = 'datos.csv'

with open(nombre_archivo, mode='w', newline='') as archivo_csv:

    writer = csv.writer(archivo_csv)

    writer.writerow(['filename', 'slug', 'path'])  # header
    writer.writerows(data_csv)  # Escribe los datos

    

# TODO
# python -m tarfile -l Union_Provincial_de_Almeria-03a731f2-3d5b-4152-a19b-7266297eab28.tar | grep "objects" > dip_objects_files.txt