from flask import Flask, render_template, request
import csv
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    disasters = []

    with open("top_10.csv", "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            disasters.append(row)

    country = None
    map_url = None
    error = None

    if request.method == "POST":

        try:

            lat = request.form["latitude"]
            lon = request.form["longitude"]

            url = "https://api.bigdatacloud.net/data/reverse-geocode-client"

            params = {
                "latitude": lat,
                "longitude": lon,
                "localityLanguage": "en"
            }

            response = requests.get(url, params=params)

            data = response.json()

            print(data)

            country = data.get("countryName", "Not Found")

            map_url = f"https://www.google.com/maps?q={lat},{lon}"

        except Exception as e:
            error = str(e)
            print(error)

    return render_template(
        "index.html",
        disasters=disasters,
        country=country,
        map_url=map_url,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)