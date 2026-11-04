from logic import WeatherFetcher


def run_app():
    # Create an instance of class WeatherFetcher
    app = WeatherFetcher()

    if app.get_city_data():
        app.fetch_weather()
        app.display_weather_info()
    else:
        print("\nFAILED TO INITIALIZE APP BECAUSE OF NETWORK ERROR")


if __name__ == '__main__':
    run_app()