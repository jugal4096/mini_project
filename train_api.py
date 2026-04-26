import requests
from datetime import datetime

url = "https://indian-railway-irctc.p.rapidapi.com/api/trains/v1/train/status"

headers = {
    "x-rapidapi-key": "f4352a8671msh053ae06f8afe072p1d0d84jsncf3856ddcbd2",
    "x-rapidapi-host": "indian-railway-irctc.p.rapidapi.com"
}

# get today's date automatically
today = datetime.now().strftime("%Y%m%d")

params = {
    "train_number": "12072",
    "departure_date": today,
    "isH5": "true",
    "client": "web",
    "deviceIdentifier": "Mozilla"
}

response = requests.get(url, headers=headers, params=params)

print(response.status_code)
print(response.json())