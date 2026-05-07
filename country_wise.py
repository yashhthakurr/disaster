import csv
with open("new1000.csv","r",encoding="utf-8") as file:
    reader = csv.DictReader(file)
    country_count = {}
    for row in reader:
        country = row["country"]
        if country in country_count:
            country_count[country] += 1
        else:
            country_count[country] = 1

with open("country_count.csv","w",newline="",encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Country", "Occurrences"])
    for country, count in country_count.items():
        writer.writerow([country, count])
print("File saved")
