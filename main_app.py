import main_logic
from main_logic import WeatherFetcher


def run_app():
    # Create an instance of class WeatherFetcher
    app = WeatherFetcher()

    if app.fetch_weather():
        app._log_options()
        app.display_weather_info()
    else:
        print("\nFAILED TO INITIALIZE APP BECAUSE OF NETWORK ERROR")

run_app()