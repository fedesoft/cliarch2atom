import csv

with open("_persons_v2.csv", "r") as fpersons:
    data = csv.reader(fpersons, delimiter='|')
    for x in data:
        if len(x[1]) > 30:
            print(x[1])