import csv
import requests

with open("global_disasters.csv","r",encoding="utf-8") as file:
    reader = csv.DictReader(file)
    filtered = []
    for row in reader:
        if row["magnitude"].strip() == "" or row["location"].strip() == "":
            continue
        row["magnitude"] = float(row["magnitude"])
        filtered.append(row)

top_1000 = sorted(filtered,
                  key=lambda row: row["magnitude"],
                  reverse=True)[:1000]

cache = {}
for row in top_1000:

    lat = row["latitude"].strip()
    lon = row["longitude"].strip()

    key = (lat, lon)

    if key in cache:
        row["country"] = cache[key]
    else:
        try:
            url = "https://api.bigdatacloud.net/data/reverse-geocode-client"
            params = {
                "latitude": lat,
                "longitude": lon,
                "localityLanguage": "en"
            }
            response = requests.get(url,params=params,timeout=5)
            data = response.json()
            country = data.get("countryName")
            if not country:
                country = data.get("locality", "Unknown")

            row["country"] = country

            cache[key] = country

            print(f"{lat}, {lon} → {country}")

        except Exception as e:

            print("Error:", e)

            row["country"] = "Unknown"

with open("new1000.csv",
          "w",
          newline="",
          encoding="utf-8") as file:

    fieldnames = top_1000[0].keys()

    writer = csv.DictWriter(file,
                            fieldnames=fieldnames)

    writer.writeheader()

    writer.writerows(top_1000)

print("Finished")