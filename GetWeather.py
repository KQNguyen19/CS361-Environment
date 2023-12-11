import json
from flask import Flask, request
import requests

app = Flask(__name__)

country = "us"
api = "6350ab23b7ea0482f09e788c444d3d62"

@app.route('/weather', methods=['GET'])
def get_weather():
    zipcode = request.args.get('zipcode')

    if not zipcode:
        return json.dumps({"error": "Zipcode is required"}), 400

    complete_url = f"http://api.openweathermap.org/data/2.5/weather?zip={zipcode},{country}&appid={api}"

    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        results = data["main"]
        description = data["weather"][0]['description']
        main = data['weather'][0]['main']
        temperature = results["temp"] * (9 / 5) - 459.67
        temperature = round(temperature, 2)
        pressure = results["pressure"]

        result = {
            "description": description,
            "main": main,
            "temperature": temperature,
            "pressure": pressure,
            "success": True
        }

        return json.dumps(result)
    else:
        return json.dumps({"error": "Invalid zipcode"}), 404

if __name__ == '__main__':
    app.run(debug=True)
