import csv
import pymssql

q_get_url = """SELECT archivo_ID, url, comentario FROM archivo.dbo.recurso WHERE url LIKE N'{url}'"""
q_archivo = "SELECT * FROM archivo.dbo.archivo WHERE ID = {archivo_id}"

conn = pymssql.connect("localhost", "SA", "<change-password>", "archivo")
cursor = conn.cursor(as_dict=True)

output = []

with open("duplicates_test.txt", "r") as fduplicates:
    dups = fduplicates.readlines()

    urls_db = []
    for line in dups:
        if line.startswith("/media/desarrollo/"):
            urls_db.append( line.split("ficheros")[1].strip() )
        
        if not line.strip():
            urls_db.append("\n")

    
for urlfile in urls_db:

    # import ipdb; ipdb.set_trace()

    if urlfile.startswith("/"):
        temp = []
        query = q_get_url.format(url=urlfile)
        cursor.execute(query)
        row = cursor.fetchall()

        # temp.append(urlfile)

        if row:
            temp.append(str(row[0]['archivo_ID']))
            temp.append(row[0]['url'])

            query2 = q_archivo.format(archivo_id=row[0]['archivo_ID'])
            cursor.execute(query2)
            row2 = cursor.fetchall()

            if row2:
                temp.append(row2[0]['clasificacion_ID'])
                temp.append(row2[0]['numerodocumento'])
            else:
                temp.append("DELETE2")

            output.append(tuple(temp))
            output.append("\n")

        else:
            temp.append(urlfile)
            temp.append("DELETE1")
            output.append(tuple(temp))
            output.append("\n")

    else:
        output.append("\n")
    
conn.close()


with open('your_file.txt', 'w') as f:
    for line in output:
        if isinstance(line, tuple):
            f.write(" || ".join(line))
        else:
            f.write("\n")
            

