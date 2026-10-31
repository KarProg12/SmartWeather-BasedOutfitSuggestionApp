import requests
from datetime import datetime

URL = "https://api.open-meteo.com/v1/forecast?latitude=53.1235&longitude=18.0076&hourly=temperature_2m,precipitation,weather_code,wind_speed_10m&timezone=auto"

now = datetime.now()
data = requests.get(URL).json()

weather = data["hourly"]

print(weather)
