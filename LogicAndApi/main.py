import requests
from datetime import datetime

API_URL = "https://api.open-meteo.com/v1/forecast?latitude=53.1235&longitude=18.0076&hourly=temperature_2m,precipitation,weather_code,wind_speed_10m&timezone=auto"

def _log_options():
    """Func for options logging. Nothing special"""
    print(f"\n[OPTIONS_LOG] >>> {weather.keys()}\n")

# Fetch JSON dict from Open-Meteo
data = requests.get(API_URL).json()
# Get hourly weather data from list 'hourly' in fetched JSON file from Open-Meteo
weather = data['hourly']

now = datetime.now()
# Fetch actual hour in format matching Open-Meteo format (e.g. "2026-10-27T21:00")
hourly_weather = now.strftime("%Y-%m-%dT%H:00")
now_date = now.strftime("%d.%m.%Y | %H:%M")

# Search on what position on list 'time' is this hour
hr_index = weather['time'].index(hourly_weather)

# --> DATA FETCHING SECTION <--
# Fetch the data for THIS exact hour
temperature = weather['temperature_2m'][hr_index]
precipitation = weather['precipitation'][hr_index]
wind_speed = weather['wind_speed_10m'][hr_index]

def display_weather_info():
    print("TEST_WEATHER_FORECAST (for the nearest hour):\n"
          "---------------------------------------------\n"
          f">>> [date format: Y-m-d-H:M] <<<\n"
          f"  DATE: {now_date}\n"
          f"  TEMPERATURE: {temperature}°C\n"
          f"  PRECIPITATION: {precipitation}mm\n"
          f"  WIND_SPEED: {wind_speed}km/h")

# --> CODE EXECUTION SECTION <--
_log_options()
display_weather_info()