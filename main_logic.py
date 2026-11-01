import requests
from datetime import datetime


class WeatherCodeTranslator:
    """Class with weather codes and their definitions as keys and vals"""
    def __init__(self):
        # Dict with: key(weather code): val(short weather code description)
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
        """Gets the description by key (weather code).
         If unknown weather code returns error message"""
        return self._WEATHER_CODES.get(weather_code, "ERROR: Unknown weather code")


class WeatherFetcher:
    """This class gets the data about weather from Open-Meteo and geocoding APIs"""
    def __init__(self):
        """Attributes are dicts in which will be stored all
        keys and vals from JSON file from Open-Meteo"""
        # There'll be stored whole JSON file
        self.data = {}
        # There'll be stored all values of key 'hourly' from JSON file
        self.hourly = {}
        self.lang_input = input("\nEnter language you want (e.g. en, pl):\n >>> ").lower().strip()
        self.city_name = input("Enter the name of the city you want to check the weather in:\n >>> ").rstrip().lstrip()
        self.URL_TO_PICK_CITY_LAT_AND_LONG = f"https://geocoding-api.open-meteo.com/v1/search?name={self.city_name}&count=1&language={self.lang_input}"
        self.city_data = {}
        self.city_name = ""
        self.latitude = ""
        self.longitude = ""
        self.API_URL = ""

    def get_city_data(self):
        """Get city's latitude and longitude by entering its name"""
        try:
            self.data = requests.get(self.URL_TO_PICK_CITY_LAT_AND_LONG).json()
            self.city_data = self.data['results'][0]
            self.city_name += self.city_data['name']
            self.latitude += str(self.city_data['latitude'])
            self.longitude += str(self.city_data['longitude'])
            self.API_URL += (
                f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&"
                "hourly=temperature_2m,precipitation,weather_code,wind_speed_10m,relative_humidity_2m&timezone=auto")
            return True
        except Exception as e:
            print(f"ERROR OF FETCHING DATA: {e}")
            # False occurs skipping the code in if statement and prints error in else statement also in main app file
            return False

    def fetch_weather(self):
        """Here's whole logic of getting data about weather from Open-Meteo"""
        try:
            # Fetch JSON dict from Open-Meteo
            self.data = requests.get(self.API_URL).json()
            self.hourly = self.data['hourly']
            # Returning True is important because it executes the code in if statement in main app file
            return True
        except Exception as e:
            print(f"ERROR OF FETCHING DATA: {e}")
            # False occurs skipping the code in if statement and prints error in else statement also in main app file
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
            humidity = self.hourly['relative_humidity_2m'][hr_index]

            # Fetching and translating weather code
            raw_weather_code = self.hourly['weather_code'][hr_index]
            translator = WeatherCodeTranslator()
            weather_description = translator.get_description(raw_weather_code)

            print("\nWEATHER_FORECAST (for the nearest hour):\n"
                  "---------------------------------------------\n"
                  f"  NAZWA_MIASTA/KRAJU:\n    {self.city_name}\n"
                  f"\n  DATA | GODZINA\n(czas lokalny urządzenia, nie sprawdzanego kraju):\n    {date_for_usr}\n"
                  f"\n  OPIS_POGODY:\n    {weather_description}\n"
                  f"\n  TEMPERATURA:\n    {temperature}°C\n"
                  f"\n  WILGOTNOŚĆ:\n    {humidity}%\n"
                  f"\n  GĘSTOŚĆ_OPADÓW:\n    {precipitation}mm\n"
                  f"\n  PRĘDKOŚĆ_WIATRU:\n    {wind_speed}km/h")

        except ValueError:
            print(f"\nERROR: HOUR {hourly_weather_time} IS OUT OF FORECAST SCOPE")
