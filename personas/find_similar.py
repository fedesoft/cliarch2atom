import csv
from thefuzz import fuzz

def nombres_similares(lista_nombres, umbral_similitud=90):

    nombres_similares = []

    for i, nombre1 in enumerate(lista_nombres):
        for j, nombre2 in enumerate(lista_nombres):
            if i != j:  # Evitar comparar el mismo nombre consigo mismo
                similitud = fuzz.ratio(nombre1, nombre2)
                if similitud >= umbral_similitud and (nombre2, nombre1) not in nombres_similares:
                    nombres_similares.append((nombre1, nombre2, similitud))

    return nombres_similares


lista_nombres = []

with open("_persons_v2.csv", "r") as fpersons:
    data = csv.reader(fpersons, delimiter='|')
    for x in data:
        lista_nombres.append(x[1])

resultados = nombres_similares(lista_nombres)

for resultado in resultados:
    print(f"{resultado[0]} ||| {resultado[1]} == {resultado[2]}%.")
