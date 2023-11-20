import json, requests
import datetime

country = "us"
api = "6350ab23b7ea0482f09e788c444d3d62"

def submit(zipcode):

    #completeUrl = "http://api.openweathermap.org/data/2.5/weather?zip=" + zipcode + "," + country + "&appid=" + api
    completeUrl = "http://api.openweathermap.org/data/2.5/weather?zip=" + zipcode + ",us&appid=" + api

    # json method of response object
    response = requests.get(completeUrl)
    data = response.json()

    # If there's no error amongst the data.
    if data["cod"] != "404":

        # Grabs the list from "Main"
        results = data["main"]

        # Grabs the description of the weather from an Associative List
        description = data["weather"][0]['description']

        # Grabs the main category of the weather from an Associative List
        main = data['weather'][0]['main']

        # Temperature is converted from Kelvin to Farenheit while rounding down in half
        temperature = results["temp"]
        temperature = temperature * (9 / 5) - 459.67
        temperature = round(temperature, 2)

        # Grabbing Atmospheric Pressure value
        pressure = results["pressure"]

        # Returns the description, main, temperature and pressure values while indicating a True flag for a correct Zipcode
        return description, main, temperature, pressure, True

    else:

        # Returns essentially no values but a False flag to indicate an error with the Zipcode
        return "", "", 0, 0, False
