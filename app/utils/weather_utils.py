import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_weather(city: str):
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "Weather API key not configured."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"].capitalize()
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            return (
                f"🌤️ Weather in {city.title()}:\n"
                f"- Condition: {desc}\n"
                f"- Temperature: {temp}°C\n"
                f"- Humidity: {humidity}%\n"
                f"- Wind Speed: {wind_speed} m/s"
            )
        else:
            return f"❌ Couldn’t fetch weather for {city.title()}. ({data.get('message', 'Unknown error')})"
    except Exception as e:
        return f"⚠️ Error fetching weather data: {str(e)}"
