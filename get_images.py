import csv
import requests
with open("./data/28k_apparel_data.csv") as f:
    csvFile = csv.reader(f)
    header = True
    for line in csvFile:
        if header:
            header = False
            continue
        url = line[4]
        id = line[0]
        print(line)
        try:
            image_data = requests.get(url).content
        except:
            print(f"INVALID LINE: {line}")
        with open(f"./data/{id}.jpeg", "wb") as handler:
            handler.write(image_data)
