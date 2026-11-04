import requests
from datetime import datetime


class WeatherCodeTranslator:
    """Class with weather codes and their definitions as keys and vals"""
    def __init__(self):
        # Dict with: key(weather code): val(short weather code description)
        self._WEATHER_CODES = {
            0: "Bezchmurnie",
            1: "Przeważnie bezchmurnie",
            2: "Częściowe zachmurzenie",
            3: "Pochmurno",

            45: "Mgła",
            48: "Mgła osadzająca szadź",

            51: "Lekka mżawka",
            53: "Umiarkowana mżawka",
            55: "Intensywna mżawka",

            56: "Lekka marznąca mżawka",
            57: "Intensywna marznąca mżawka",

            61: "Lekki deszcz",
            63: "Umiarkowany deszcz",
            65: "Silny deszcz",

            66: "Lekki marznący deszcz",
            67: "Silny marznący deszcz",

            71: "Lekki opad śniegu",
            73: "Umiarkowany opad śniegu",
            75: "Silny opad śniegu",

            77: "Ziarna śniegu",

            80: "Słabe przelotne opady deszczu",
            81: "Umiarkowane przelotne opady deszczu",
            82: "Gwałtowne przelotne opady deszczu",

            85: "Słabe przelotne opady śniegu",
            86: "Intensywne przelotne opady śniegu",

            95: "Burza",
            96: "Burza z lekkim gradem",
            97: "Silna burza",
            99: "Burza z silnym gradem"
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
        self.API_URL = ""

    def get_city_data(self):
        """Get city's latitude and longitude by entering its name"""
        try:
            self.data = requests.get(self.URL_TO_PICK_CITY_LAT_AND_LONG).json()
            self.city_data = self.data['results'][0]
            self.city_name = self.city_data['name']
            latitude = str(self.city_data['latitude'])
            longitude = str(self.city_data['longitude'])
            self.API_URL = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,apparent_temperature,precipitation,precipitation_probability,rain,showers,snowfall,snow_depth,weather_code,wind_speed_10m,wind_direction_10m,relative_humidity_2m,dewpoint_2m,pressure_msl,cloud_cover,visibility&timezone=auto"
            print(f"\n  Weather data root (Bydgoszcz coordinates by default):\n       {self.API_URL}")
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
            apparent_temperature = self.hourly['apparent_temperature'][hr_index]
            precipitation = self.hourly['precipitation'][hr_index]
            precipitation_probability = self.hourly['precipitation_probability'][hr_index]
            rain = self.hourly['rain'][hr_index]
            showers = self.hourly['showers'][hr_index]
            snowfall = self.hourly['snowfall'][hr_index]
            snow_depth = self.hourly['snow_depth'][hr_index]
            cloud_cover = self.hourly['cloud_cover'][hr_index]
            visibility = self.hourly['visibility'][hr_index]
            visibility_unit = ""
            if visibility >= 1000:
                visibility = visibility / 1000
                visibility_unit = "km"
            elif visibility < 1000:
                visibility = visibility
                visibility_unit = "m"
            wind_speed = self.hourly['wind_speed_10m'][hr_index]
            wind_direction = self.hourly['wind_direction_10m'][hr_index]
            wind_direction_name = ""
            if 337.5 <= wind_direction <= 360 or 0 <= wind_direction < 22.5:
                wind_direction_name = "N"
            elif 22.5 <= wind_direction < 67.5:
                wind_direction_name = "NE"
            elif 67.5 <= wind_direction < 112.5:
                wind_direction_name = "E"
            elif 112.5 <= wind_direction < 157.5:
                wind_direction_name = "SE"
            elif 157.5 <= wind_direction < 202.5:
                wind_direction_name = "S"
            elif 202.5 <= wind_direction < 247.5:
                wind_direction_name = "SW"
            elif 247.5 <= wind_direction < 292.5:
                wind_direction_name = "W"
            elif 292.5 <= wind_direction < 337.5:
                wind_direction_name = "NW"
            relative_humidity = self.hourly['relative_humidity_2m'][hr_index]
            dewpoint = self.hourly['dewpoint_2m'][hr_index]
            atmospheric_pressure = self.hourly['pressure_msl'][hr_index]

            # Fetching and translating weather code
            raw_weather_code = self.hourly['weather_code'][hr_index]
            translator = WeatherCodeTranslator()
            weather_description = translator.get_description(raw_weather_code)


            print("\n----------------------------------------\n"
		  "WEATHER_FORECAST (for the nearest hour):\n"
                  "----------------------------------------\n"
                  f"  NAZWA_MIASTA/KRAJU:\n    {self.city_name}\n"
                  f"  DATA | GODZINA\n(czas lokalny urządzenia, nie sprawdzanego kraju):\n    {date_for_usr}\n"
                  f"  OPIS_POGODY:\n    {weather_description}\n"
                  f"  ZACHMURZENIE:\n    {cloud_cover}%\n"
                  f"  WIDOCZNOŚĆ:\n    {visibility}{visibility_unit}\n"
                  f"  TEMPERATURA:\n    {temperature}°C\n"
                  f"  TEMPERATURA_ODCZUWALNA:\n    {apparent_temperature}°C\n"
                  f"  WILGOTNOŚĆ:\n    {relative_humidity}%\n"
                  f"  PUNKT_ROSY:\n    {dewpoint}°C\n"
                  f"  PRAWDOPODOBIEŃSTWO_OPADÓW:\n    {precipitation_probability}%\n"
                  f"  SUMA_WSZELKICH_OPADÓW:\n    {precipitation}mm\n"
                  f"  OPADY_PRZELOTNE:\n    {showers}mm\n"
                  f"  OPAD_DESZCZU:\n    {rain}mm\n"
                  f"  OPAD_ŚNIEGU:\n    {snowfall}cm\n"
                  f"  GRUBOŚĆ_POKRYWY_ŚNIEŻNEJ:\n    {snow_depth}m\n"
                  f"  CIŚNIENIE_ATMOSFERYCZNE:\n    {atmospheric_pressure}hPa\n"
                  f"  KIERUNEK_WIATRU:\n    {wind_direction}° ({wind_direction_name})\n"
                  f"  PRĘDKOŚĆ_WIATRU:\n    {wind_speed}km/h")

        except ValueError:
            print(f"\nERROR: HOUR {hourly_weather_time} IS OUT OF FORECAST SCOPE")
