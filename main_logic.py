import requests
from datetime import datetime


class WeatherCodeTranslator:
    def __init__(self):
        self._WEATHER_CODES = {
            0: "Słonecznie, bezchmurnie",
            1: "Przejaśnienia, prawie bezchmurnie",
            2: "Umiarkowane, częściowe zachmurzenie",
            3: "Zachmurzenie całkowite, pochmurno",
            45: "Mgła, zamglenie",
            48: "Marznąca mgła, mgła osadzająca szron",
            51: "Lekka mżawka, słaby opad mżawki",
            53: "Mżawka, umiarkowana mżawka",
            55: "Silna mżawka, intensywna mżawka",
            61: "Lekki deszcz, słaby deszcz",
            63: "Deszcz, umiarkowany deszcz",
            65: "Silny deszcz, ulewa",
            71: "Lekki śnieg, słabe opady śniegu",
            73: "Śnieg, umiarkowane opady śniegu",
            75: "Silny śnieg, śnieżyca",
            77: "Śnieg ziarnisty, krupa śnieżna",
            80: "Przelotny deszcz, przelotny opad",
            81: "Przelotny deszcz, silny opad przelotny",
            82: "Ulewa, gwałtowny deszcz przelotny",
            85: "Przelotny śnieg",
            86: "Śnieżyca przelotna",
            95: "Burza, burza z piorunami",
            96: "Burza z gradem",
            99: "Gwałtowna burza, silna burza z gradem",
        }

    def get_description(self, weather_code):
        """Fetches the description. If weather code is unknown returns error message"""
        return self._WEATHER_CODES.get(weather_code, "ERROR: Unknown weather code")


class WeatherFetcher:
    API_URL = "https://api.open-meteo.com/v1/forecast?latitude=53.1235&longitude=18.0076&hourly=temperature_2m,precipitation,weather_code,wind_speed_10m&timezone=auto"

    def __init__(self):
        self.data = {}
        self.hourly = {}

    def fetch_weather(self):
        try:
            # Fetch JSON dict from Open-Meteo
            response = requests.get(self.API_URL)
            self.data = response.json()
            self.hourly = self.data['hourly']
            return True
        except Exception as e:
            print(f"ERROR OF FETCHING DATA: {e}")
            return False

    def _log_options(self):
        """Func for options logging for dev. Nothing special"""
        if not self.data:
            print("\nTHERE'S NOTHING TO LOG.\nUSE fetch_weather() FIRST")

        print(f"\n!!! THESE LOGS ARE ONLY FOR DEV !!!\n"
              f"===================================\n"
              f"[ALL_OPTIONS_LOG]\n >>> {list(self.data.keys())}\n"
              f"[WEATHER_OPTIONS_LOG]\n >>> {list(self.hourly.keys())}\n"
              f"===================================\n\n"
              f"###############-APP-###############")

    def display_weather_info(self):
        if not self.hourly:
            print("\nNO DATA TO DISPLAY")

        now = datetime.now()
        hourly_weather_time = now.strftime('%Y-%m-%dT%H:00')
        date_for_usr = now.strftime('%d.%m.%Y | %H:%M')

        try:
            # Find the position of current hour on the 'time' list
            hr_index = self.hourly['time'].index(hourly_weather_time)

            # Fetching data for found hour index
            temperature = self.hourly['temperature_2m'][hr_index]
            precipitation = self.hourly['precipitation'][hr_index]
            wind_speed = self.hourly['wind_speed_10m'][hr_index]

            # Fetching and translating weather code
            raw_code = self.hourly['weather_code'][hr_index]
            translator = WeatherCodeTranslator()
            weather_description = translator.get_description(raw_code)

            print("\nWEATHER_FORECAST (for the nearest hour):\n"
                  "---------------------------------------------\n"
                  f"  DATE: {date_for_usr}\n"
                  f"  WHAT_WEATHER: {weather_description}\n"
                  f"  TEMPERATURE: {temperature}°C\n"
                  f"  PRECIPITATION: {precipitation}mm\n"
                  f"  WIND_SPEED: {wind_speed}km/h")

        except ValueError:
            print(f"\nERROR: HOUR {hourly_weather_time} IS OUT OF FORECAST SCOPE")
