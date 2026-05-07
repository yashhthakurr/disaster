import csv
country_year_count = {}
with open("new1000.csv","r",encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        date = row["date"].strip()
        country = row["country"].strip()

        if date == "" or country == "":
            continue
        try:

            year = date.split("-")[0]

            key = (year, country)

            if key in country_year_count:
                country_year_count[key] += 1
            else:
                country_year_count[key] = 1
        except Exception as e:
            print("Error:", e)

with open("country_year_trend.csv","w",newline="",encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Year","Country","Earthquake_Count"])
    for (year, country), count in sorted(country_year_count.items()):
        writer.writerow([year,country,count])
print("Country-year trend saved.")