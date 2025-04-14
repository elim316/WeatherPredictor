

import json
import os

# Debugging statements 
# print(os.getcwd())

# def get_station(filename):

#     def read_json(filename):
#         with open(filename, 'r') as read_file:
#             try:
#                 if read_file is not None:
#                     obj = json.load(read_file)
#                     # print(obj)
#                     pretty_json = json.dumps(obj, indent=4) # noticed that it updates the json after every call
#                     print(pretty_json)
#             except json.decoder.JSONDecodeError:
#                 print("Error: File is empty or not a valid JSON file.")
#             except FileNotFoundError:
#                 print("Error: File not found.")
    
#     def parse_json(filename):
#         with open(filename) as f:
#            data = json.load(f)

#         for station in data.get("data", {}).get("stations", []):
#             print(station.get("name"))

#     read_json(filename)
#     parse_json(filename)

def get_station(filename):
    station_names = []
    with open(filename) as f:
        data = json.load(f)

    for station in data.get("data", {}).get("stations", []):
        station_name = station.get("name")
        station_names.append(station_name)
    
    return station_names


humidity_station = get_station("Data/HumidityData.json")
rainfall_station = get_station("Data/RainfallData.json")
windspeed_station = get_station("Data/WindSpeedData.json")
airtemperature_station = get_station("Data/AirTemperatureData.json")


common = list(set(humidity_station) & set(rainfall_station) & set(windspeed_station) & set(airtemperature_station))
common.sort()
print("Common Stations:")
for station in common:
    print(station)
print("Number of Common Stations: ", len(common))

'Common Stations:'
'Ang Mo Kio'
'Jurong Island'
'Clementi'
'East Coast Parkway'
'Taiseng'
'Jurong (West)'
'Pulau ubin'
'Somerset(road)'
'Tuas south'
'Ulu Pandan'
'Admiralty (West)'


    