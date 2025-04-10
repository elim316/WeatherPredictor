import json
import os

def read_json(filename):
    with open(filename, "r") as read_file:
        obj = json.load(read_file)
        pretty_json = json.dumps(obj, indent=4)
        print(pretty_json)
    
    try:
        with open(filename, "r") as read_file:
            obj = json.load(read_file)
            pretty_json = json.dumps(obj, indent=4)
            print(pretty_json)

    except json.decoder.JSONDecodeError:
        print("Error: File is empty or not a valid JSON file.")
    except FileNotFoundError:
        print("Error: File not found.")

'Debugging statements'
# print('Current Working Directory:', os.getcwd())
# print('Files in Current Working Directory:', os.listdir(os.getcwd()))
# print("Real File Path:" + os.path.realpath(__file__))

print("Humidity Data")
# read_json("Data/HumidityData.json")
print("Wind Speed Data")
# read_json("Data/WindSpeedData.json")
print("Rainfall Data")
# read_json("Data/RainfallData.json")