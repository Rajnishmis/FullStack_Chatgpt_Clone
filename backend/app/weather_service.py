# backend/app/services/weather_service.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
OWM_KEY = os.getenv("OPENWEATHERMAP_KEY")
OWM_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather_by_city(city: str):
    """
    Calls OpenWeatherMap API and returns a friendly string or raises Exception on failure.
    """
    if not OWM_KEY:
        raise RuntimeError(
            "OpenWeatherMap API key not configured (OPENWEATHERMAP_KEY).")

    params = {"q": city, "appid": OWM_KEY, "units": "metric"}
    resp = requests.get(OWM_URL, params=params, timeout=10)

    if resp.status_code != 200:
        # propagate detailed message
        raise ValueError(
            f"OpenWeatherMap error: {resp.status_code} - {resp.text}")

    data = resp.json()
    # Extract useful information
    name = data.get("name", city)
    weather_desc = data["weather"][0]["description"] if data.get(
        "weather") else "No description"
    temp = data["main"]["temp"] if data.get("main") else None
    feels_like = data["main"].get("feels_like") if data.get("main") else None
    humidity = data["main"].get("humidity") if data.get("main") else None

    parts = []
    if temp is not None:
        parts.append(f"{temp}°C")
    if feels_like is not None:
        parts.append(f"(feels like {feels_like}°C)")
    if humidity is not None:
        parts.append(f"humidity {humidity}%")

    temp_part = ", ".join(parts) if parts else "No temperature data"

    friendly = f"The weather in {name} is {weather_desc} with a temperature of {temp_part}."
    return friendly
