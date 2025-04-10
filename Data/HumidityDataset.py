import requests
import json
import os

print('Current Working Directory:', os.getcwd())

url = "https://api-open.data.gov.sg/v2/real-time/api/relative-humidity"

response = requests.get(url)

data = response.json()

# Save to a file
with open('/Users/elias/Documents/GitHub/WeatherPredictor/Data/HumidityData.json', 'w') as file:
    json.dump(data, file, indent=4)

# Print pretty JSON
pretty_json = json.dumps(data, indent=4)
# print(pretty_json)

