import requests

API_URL = "https://api.open-meteo.com/v1/forecast?latitude=53.1235&longitude=18.0076&hourly=temperature_2m,precipitation,weather_code,wind_speed_10m&timezone=auto"

data = requests.get(API_URL).json()
weather = data['hourly']

def _log_options():
    print("\n|----------------------------------------------------------------------------------------------------------|\n"
          f"[OPTIONS_LOG] >>> {weather.keys()} |\n"
          "|----------------------------------------------------------------------------------------------------------|\n")

_log_options()

temperature = weather['temperature_2m'][0]
precipitation = weather['precipitation'][0]

print("TEST_WEATHER_FORECAST (for the nearest hour):\n"
      f"TEMPERATURE: {temperature}°C\n"
      f"PRECIPITATION: {precipitation}mm")

