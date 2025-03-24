from typing import Any, Dict, Optional

import aiohttp

from ..config.settings import settings


class WeatherAPI:
    """Wrapper for OpenWeather API."""

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Weather API wrapper."""
        self.api_key = api_key or settings.OPENWEATHER_API_KEY
        if not self.api_key:
            raise ValueError("OpenWeather API key is required")

    async def get_weather(self, city: str) -> Dict[str, Any]:
        """Get current weather for a city."""
        params = {"q": city, "appid": self.api_key, "units": "metric"}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.BASE_URL}/weather", params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed to get weather: {await response.text()}")

    async def get_forecast(self, city: str) -> Dict[str, Any]:
        """Get 5-day forecast for a city."""
        params = {"q": city, "appid": self.api_key, "units": "metric"}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.BASE_URL}/forecast", params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed to get forecast: {await response.text()}")


class FlightAPI:
    """Wrapper for Flight data API."""

    BASE_URL = "https://aeroapi.flightaware.com/aeroapi"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Flight API wrapper."""
        self.api_key = api_key or settings.FLIGHTAWARE_API_KEY
        if not self.api_key:
            raise ValueError("FlightAware API key is required")

    async def get_flight_info(self, flight_number: str) -> Dict[str, Any]:
        """Get information about a specific flight."""
        headers = {"x-apikey": self.api_key}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.BASE_URL}/flights/{flight_number}", headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed to get flight info: {await response.text()}")

    async def get_airport_delays(self, airport_code: str) -> Dict[str, Any]:
        """Get delay information for an airport."""
        headers = {"x-apikey": self.api_key}
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.BASE_URL}/airports/{airport_code}/delays", headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed to get airport delays: {await response.text()}")


class NotificationAPI:
    """Wrapper for Twilio notification API."""

    def __init__(self, account_sid: Optional[str] = None, auth_token: Optional[str] = None):
        """Initialize the Notification API wrapper."""
        self.account_sid = account_sid or settings.TWILIO_ACCOUNT_SID
        self.auth_token = auth_token or settings.TWILIO_AUTH_TOKEN
        if not self.account_sid or not self.auth_token:
            raise ValueError("Twilio account SID and auth token are required")

        # Lazy import twilio to avoid dependency issues
        try:
            from twilio.rest import Client

            self.client = Client(self.account_sid, self.auth_token)
        except ImportError:
            raise ImportError("Twilio package is required for notifications")

    def send_sms(self, to: str, message: str, from_: Optional[str] = None) -> Dict[str, Any]:
        """Send an SMS notification."""
        # You would need to set up a Twilio phone number
        from_ = from_ or "+1234567890"  # Replace with default Twilio number

        message = self.client.messages.create(body=message, from_=from_, to=to)

        return {"sid": message.sid, "status": message.status, "to": message.to, "from": message.from_}

    async def send_email(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        """Send an email notification (placeholder - would need an email service)."""
        # This is a placeholder - you'd need to implement using an email service
        # You could use SendGrid, Mailgun, or a similar service
        print(f"Sending email to {to} with subject '{subject}'")
        return {"to": to, "subject": subject, "status": "sent"}
