import requests
import json
import os

# print('Current Working Directory:', os.getcwd())
# print('Files in Current Working Directory:', os.listdir(os.getcwd()))
subdir = 'Data'
dict = dict(enumerate(os.scandir(subdir)))
print(dict)

url = "https://api-open.data.gov.sg/v2/real-time/api/air-temperature"

response = requests.get(url)

data = response.json()

# Save to a file
with open('/Users/elias/Documents/GitHub/WeatherPredictor/Data/AirTemperatureData.json', 'w') as file:
# with os.open(dict[4], 'w') as file:
    json.dump(data, file, indent=4)

print(response.json())