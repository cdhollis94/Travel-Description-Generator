# Chris Hollis
# A program that uses data from APIs to create a written description of two locations: a point of
# departure and a destination. The amount of time required to travel from one city to the other is
# taken into account.

import requests
import json


class City:
    temp = feelsTemp = windSpeed = gustSpeed = cloudCover = isDay = rainInches = humidity = visibilityRange = 0
    season = windDirection = weather = time = name = state = ""
    travel_time = 0
    timeEpoch = 0
    travel_distance = ""
    travel_distance_int = 0

    def init_weather_data(self, json_data):
        """initializes the weather data members for a city"""
        self.timeEpoch = json_data['location']['localtime_epoch']
        self.name = json_data['location']['name']
        self.state = json_data['location']['region']
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
        month = int(self.time[5] + self.time[6])
        if month == 12 or month <= 2:
            self.season = "Winter"
        elif month <= 5:
            self.season = "Spring"
        elif month <= 8:
            self.season = "Summer"
        else:
            self.season = "Autumn"

    def init_arrival_data(self, arrival_data, travel_distance):
        self.temp = arrival_data['temp_f']
        self.feelsTemp = arrival_data['feelslike_f']
        self.windSpeed = arrival_data['wind_mph']
        self.windDirection = arrival_data['wind_dir']
        self.gustSpeed = arrival_data['gust_mph']
        self.cloudCover = arrival_data['cloud']
        self.weather = arrival_data['condition']['text']
        self.isDay = arrival_data['is_day']
        self.rainInches = arrival_data['precip_in']
        self.humidity = arrival_data['humidity']
        self.time = arrival_data['time']
        self.visibilityRange = arrival_data['vis_miles']
        month = int(self.time[5] + self.time[6])
        if month == 12 or month <= 2:
            self.season = "Winter"
        elif month <= 5:
            self.season = "Spring"
        elif month <= 8:
            self.season = "Summer"
        else:
            self.season = "Autumn"
        self.travel_distance = travel_distance
        i = 0
        temp_string = ""
        while travel_distance[i] != ' ':
            if travel_distance[i] != ',':
                temp_string += travel_distance[i]
            i += 1
        self.travel_distance_int = int(temp_string)


def json_print(obj):
    """creates a formatted string of a JSON object"""
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def paragraph_print(paragraph):
    """formats the paragraph to fit within the console"""
    line_break_count = 0
    for char in paragraph:
        if line_break_count >= 120:
            if char == ' ':
                print()
                line_break_count = 0
            else:
                print(char, end='')
                line_break_count += 1
        else:
            print(char, end='')
            line_break_count += 1
    print()


def enter_cities(city, city2):
    """retrieves data from the web about inputted cities"""
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
            city.init_weather_data(depart_data)                # enter json data into class object
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
                'http://api.weatherapi.com/v1/forecast.json?key=' + weather_key + '&q=' + destination_city
                + '&days=7').json()
            print("City accepted.")
            valid_city = True
            city2.init_weather_data(destination_data)           # enter json data into class object
        else:
            print("Please enter a city in the U.S.")
    depart_lon = str(depart_data['location']['lon'])
    depart_lat = str(depart_data['location']['lat'])
    dest_lon = str(destination_data['location']['lon'])
    dest_lat = str(destination_data['location']['lat'])
    travel_data = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='
                               + depart_lat + ',' + depart_lon + '&destinations=' + dest_lat + ',' + dest_lon
                               + '&key=' + travel_key).json()
    travel_time = travel_data["rows"][0]["elements"][0]["duration"]["value"]            # additional travel variables
    travel_distance = travel_data["rows"][0]["elements"][0]["distance"]["text"] + "les"
    arrival_time = city.timeEpoch + travel_time
    # Adjust destination data to account for travel time---------------------------------------------------------------
    for j in range(5):
        for i in range(24):
            if destination_data['forecast']['forecastday'][j]['hour'][i]['time_epoch'] >= arrival_time:
                arrival_data = destination_data['forecast']['forecastday'][j]['hour'][i]
                city2.init_arrival_data(arrival_data, travel_distance)
                return


def generate_paragraphs(city, is_destination):
    """writes a paragraph based on the weather data for the provided city"""
    count = 0
    is_cooler = False
    is_hot = False
    if city.feelsTemp > 90:
        is_hot = True
    p = ""
    # Departure City--------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------
    if is_destination:
        p += "With the metal sign on the side of the road growing smaller behind you, you reach your destination. "
    if city.cloudCover == 0:
        p += "A cloudless "
        if city.isDay:
            p += ("day in " + city.name + ", ")
        else:
            p += ("night in " + city.name + ", ")
        if city.windSpeed != 0:
            p += "but with wind willing to ferry them around had they been there. "
        elif city.gustSpeed != 0:
            p += "but with a temporary gust. It arrived like a drifter seeking employ, but seeing no clouds to " \
                 "chauffeur it would soon depart. "
        else:
            p += "and with no wind, either. The sky was still, waiting for something to stir it. "
    elif city.rainInches != 0:
        p += "It is a rainy "
        if city.isDay:
            p += ("day in " + city.name + ", ")
        else:
            p += ("night in " + city.name + ", ")
        if city.windSpeed >= 20 or city.gustSpeed >= 20:
            p += "fraught with violence. A ruthless wind hurls droplets senselessly, shattering them against the " \
                 "city's surface. "
        elif city.windSpeed != 0 or city.gustSpeed != 0:
            p += "with an impish wind nudging droplets, deviating their trajectories and places of impact from " \
                 "the clouds' intention. "
        else:
            p += "with each droplet careening towards the city unaffected, perfectly beneath its birthplace and " \
                 "unmoved by wind. "
    elif city.windSpeed > 17:
        p += "It's a windy "
        if city.isDay:
            p += ("day in " + city.name + ", ")
        else:
            p += ("night in " + city.name + ", ")
        if city.cloudCover == 0:
            p += "though the sky couldn't tell you that. Concealed by the lack of clouds, the wind passed through " \
                 "the air above the city invisibly, leaping from building top to building top. "
        elif city.humidity >= 60:
            p += "as blocks of thick air collided with faces, flags, and fenced-off properties. The general " \
                 "thickness of the place might not be easily attributed to the wetness of the air, but its weight " \
                 "bore heavy on the thoughts of city's current inhabitants. "
    else:
        if city.isDay:
            p += (city.name + " daytime. ")
        else:
            p += (city.name + " nighttime. ")
    # -----------------------------------------------------------------------------------------------------------------
    if city.visibilityRange < 8 and count < 3:
        count += 1
        p += "The eye can't see as far as it should today, be it from dust or smog or any other gaseous concealer, " \
             "but the city surely extends far beyond what is currently visible. "
    if city.temp - city.feelsTemp > 7 and count < 3:
        count += 1
        p += "It's much warmer than the thermometers would lead you to believe, as if their red, alcoholic " \
             "contents grew weary from their climb a mere " + str(int(city.temp - city.feelsTemp)) + " degrees " \
             "from their destination. "
    elif city.temp - city.feelsTemp < -6 and (city.windSpeed > 15 or city.gustSpeed > 15) and count < 3:
        count += 1
        p += "Wind flows through the streets, slipping undetected by thermometers but making itself known to the " \
             "skin of pedestrians and passerby. "
        if city.temp >= 88:
            p += "Right now it comes to them as a relief, but this is not always the case. "
        elif city.temp <= 50:
            p += "They glance at the gauges and wish that the measurements felt true as blades of frigid " \
                 "air trade glancing blows against the curves of their cheeks. "
    elif city.temp - city.feelsTemp < -4 and count < 3:
        count += 1
        is_cooler = True
        if city.temp > 80:
            p += "The whole scene doesn't feel as hot as it ought to, though this can't be attributed to the " \
                 "wind's efforts "
            if city.isDay:
                p += "today. "
            else:
                p += "tonight. "
        else:
            p += "The whole scene feels colder than it ought to, though the usual suspect could not be at fault as " \
                 "it is not a particularly windy "
            if city.isDay:
                p += "day. "
            else:
                p += "night. "
    if city.windSpeed != 0 or city.gustSpeed != 0:
        count += 1
        p += "The breeze is "
        if 0 < city.windSpeed < 5 or 0 < city.gustSpeed < 5:
            p += "weakly pushing "
        else:
            p += "forcibly dragging "
        p += "fallen leaves across "
        if city.isDay:
            p += "sunlit "
        else:
            p += "moonlit "
        p += "streets. "
        if city.windDirection == 'N' or "NE" or "NW":
            if city.windSpeed > 15 or city.gustSpeed > 15:
                p += "Like an excited tourist it lands in the city from the south, seeing all the sights in a " \
                     "single flyby before lifting off northward"
            else:
                p += "It lazily reaches the city from the south and exits northward"
            if city.state in {"Washington", "Idaho", "Montana", "North Dakota", "Wisconsin", "New York", "Vermont",
                              "New Hampshire", "Maine"}:
                p += " towards Canada. "
            elif city.state == "Michigan":
                p += " across the waters of the Great Lakes. "
            else:
                p += " into neighboring states. "
        elif city.windDirection == "S" or "SE" or "SW":
            p += "It arrives from the north before setting out southward"
            if city.state in {"California", "Arizona", "New Mexico", "Texas"}:
                p += " towards Mexico. "
            elif city.state in {"Louisiana", "Mississippi", "Alabama", "Florida", "Georgia"}:
                p += " over the waves of the Gulf of Mexico. "
            else:
                p += " into the state below. "
    if city.cloudCover >= 50 and count < 3:
        count += 1
        p += "A majority of the sky is covered in clouds, "
        if city.isDay:
            p += "their amorphous, pale bodies billowing to and fro, expanding and contracting"
            if is_hot:
                p += " yet failing to shield the city from the sun's heavy rays. "
            else:
                p += ". "
        else:
            p += "and with it being nighttime it is occasionally difficult to discern if a particular patch " \
                 "of it is covered or not, due to the general blackness of either option. "
    if city.feelsTemp > 92 and count < 3:
        count += 1
        if is_cooler:
            p += "It's still burning hot: even the locals agree"
        else:
            p += "It's burning hot: even the locals agree"
        if city.season == "Summer":
            p += ". They resign that it should be expected during the Summer months, though this brings " \
                 "them no relief. "
        elif city.season == "Spring":
            p += ", and they moan that it feels as if Summer is coming earlier each year. "
        elif city.season == "Winter":
            p += ". They wring their hands and glance momentarily at calendars wondering when it will truly begin " \
                 "to feel like Winter again. "
        else:
            p += ". "
    elif city.temp < 32 and count < 3:
        count += 1
        p += "It is officially below the freezing point, and everyone in the city knows it. Hands move across each " \
             "other like pistons and blankets are stretched from neck to toes. "
    elif city.temp < 45 and count < 3:
        count += 1
        p += "The people breath swirls of gray, cartwheeling vapor out into the air. They tumble about for a second " \
             "or so before wandering too far and vanishing into the cold space. "
    if 0 < city.cloudCover <= 15 and count < 3:
        count += 1
        p += "A handful of clouds make their way through the airspace above the city to a destination only they know. "
    return p


def build_story(city1, city2, intermission):
    print()
    paragraph_print(generate_paragraphs(city1, False))
    print()
    print(intermission)
    print()
    paragraph_print(generate_paragraphs(city2, True))
    print()


# Execution Begins -------------------------------------------------------------------------------------
start_city = City()
end_city = City()
enter_cities(start_city, end_city)
intermission = "The road beneath you zips by, with " + str(int(end_city.travel_distance_int/2)) \
               + " of it left. Halfway there."
build_story(start_city, end_city, intermission)


