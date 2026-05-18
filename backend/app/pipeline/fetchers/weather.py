import httpx
from app.core.config import settings
from typing import Dict, Any

class WeatherFetcher:
    def __init__(self):
        self.api_key = settings.OPENWEATHERMAP_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
    async def fetch_current_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Fetches current weather for a specific latitude and longitude.
        """
        url = f"{self.base_url}/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"  # For Celsius
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Error fetching weather data for ({lat}, {lon}): {e}")
                return {}
            except Exception as e:
                print(f"Unexpected error in weather fetcher: {e}")
                return {}

    async def fetch_forecast(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Fetches 5-day forecast (3-hour steps) for a specific latitude and longitude.
        """
        url = f"{self.base_url}/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Error fetching forecast data for ({lat}, {lon}): {e}")
                return {}
