# Chris Hollis
# A program that uses data from APIs to create a written description of two locations: a point of
# departure and a destination. The amount of time required to travel from one city to the other is
# taken into account.

import requests
import json


class City:
    temp = feelsTemp = windSpeed = gustSpeed = cloudCover = isDay = rainInches = humidity = visibilityRange = 0
    windDirection = weather = time = ""

    def init_weather_data(self, json_data):
        """initializes the weather data members for a city"""
        self.temp = json_data['current']['temp_f']
        self.feelsTemp = json_data['current']['feelslike_f']
        self.windSpeed = json_data['current']['wind_mph']
        self.windDirection = json_data['current']['wind_dir']
        self.gustSpeed = json_data['current']['gust_mph']
        self.cloudCover = json_data['current']['cloud']
        self.weather = json_data['current']['condition']['text']
        self.isDay = json_data['current']['is_day']
        self.rainInches = json_data['current']['precip_in']
        self.humidity = json_data['current']['humidity']
        self.time = json_data['current']['last_updated']
        self.visibilityRange = json_data['current']['vis_miles']


def json_print(obj):
    """creates a formatted string of a JSON object"""
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def enter_cities(city1, city2):
    weather_key = 'eeb78f269fa54f04bd160750202709'
    travel_key = 'AIzaSyBfca4VeM9H4jRYAWkPK4NYG5BX1TyC4ks'
    valid_city = False
    print("Enter a city to set as your point of departure.")
    while valid_city is False:
        depart_city = input()
        depart_data = requests.get(
            'http://api.weatherapi.com/v1/search.json?key=' + weather_key + '&q=' + depart_city).json()
        if depart_data[0]['region'] == "Hawaii":
            print("Unfortunately, cities in Hawaii are not accepted.")
        elif depart_data[0]['region'] == "Alaska":
            print("Unfortunately, cities in Alaska are not accepted.")
        elif depart_data[0]['country'] == "United States of America":
            depart_data = requests.get(
                'http://api.weatherapi.com/v1/current.json?key=' + weather_key + '&q=' + depart_city).json()
            print("City accepted.")
            valid_city = True
            city1.init_weather_data(depart_data)                # enter json data into class object
        else:
            print("Please enter a city in the U.S.")
    print("Enter a city to set as your destination.")
    valid_city = False
    while valid_city is False:
        destination_city = input()
        destination_data = requests.get(
            'http://api.weatherapi.com/v1/search.json?key=' + weather_key + '&q=' + destination_city).json()
        if destination_data[0]['region'] == "Hawaii":
            print("Unfortunately, cities in Hawaii are not accepted.")
        elif destination_data[0]['region'] == "Alaska":
            print("Unfortunately, cities in Alaska are not accepted.")
        elif destination_data[0]['country'] == "United States of America":
            destination_data = requests.get(
                'http://api.weatherapi.com/v1/current.json?key=' + weather_key + '&q=' + destination_city).json()
            print("City accepted.")
            valid_city = True
            city2.init_weather_data(destination_data)           # enter json data into class object
        else:
            print("Please enter a city in the U.S.")
    json_print(depart_data)
    depart_lon = str(depart_data['location']['lon'])
    depart_lat = str(depart_data['location']['lat'])
    dest_lon = str(destination_data['location']['lon'])
    dest_lat = str(destination_data['location']['lat'])
    travel_data = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='
                               + depart_lat + ',' + depart_lon + '&destinations=' + dest_lat + ',' + dest_lon
                               + '&key=' + travel_key).json()
    json_print(travel_data)


# Execution Begins -------------------------------------------------------------------------------------
start_city = City()
end_city = City()
enter_cities(start_city, end_city)


