import requests
from datetime import datetime

API_URL = "https://api.open-meteo.com/v1/forecast?latitude=53.1235&longitude=18.0076&hourly=temperature_2m,precipitation,weather_code,wind_speed_10m&timezone=auto"

# Fetch JSON dict from Open-Meteo
data = requests.get(API_URL).json()
# Get hourly weather data from list 'hourly'
weather = data['hourly']

def _log_options():
    """Func for options logging. Nothing special"""
    print("\n|----------------------------------------------------------------------------------------------------------|\n"
          f"[OPTIONS_LOG] >>> {weather.keys()} |\n"
          "|----------------------------------------------------------------------------------------------------------|\n")

_log_options()

temperature = weather['temperature_2m'][0]
precipitation = weather['precipitation'][0]

print("TEST_WEATHER_FORECAST (for the nearest hour):\n"
      f"TEMPERATURE: {temperature}°C\n"
      f"PRECIPITATION: {precipitation}mm")

# Fetch actual hour in format matching Open-Meteo (e.g. "2026-10-27T21:00"
now = datetime.now().strftime("%Y-%m-%dT%H:00")

# Search on what position on list 'time' is this hour
hr_index = weather['time'].index(now)

# Fetch the data for THIS exact hour
temperature = weather['temperature_2m'][hr_index]

print(f"DATE ([format: Y-m-d-H:00]\n(here always will be full four because it's a hourly forecast): {now}")