This Readme contains the instructions to using the GetWeather Module in Python.

In order for the Microservice to work. The user must submit a valid United States Zipcode (5 Digits) in order to receive data for viewing.
For an Example, in the Drone file, the user enters in a valid 5 digit Zipcode and presses the Submit button. This calls on the GetWeather module to get a JSON Response to Open Weather API.

The provided results are strings of the "Main Weather", a "Description" of the weather and Integer values for the Temperature and Atmospheric Pressure. If the user gives a faulty Zipcode, 
the program will fail and prompt for another zipcode to be used.
