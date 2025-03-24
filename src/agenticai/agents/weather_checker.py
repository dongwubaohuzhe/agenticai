from typing import Any, Dict

from .base import AgentConfig, BaseAgent


class WeatherCheckerAgent(BaseAgent):
    """Agent responsible for checking weather conditions at airports."""

    def __init__(self):
        config = AgentConfig(
            name="WeatherChecker",
            role="Weather Analysis Specialist",
            goal="Accurately assess weather conditions at airports to predict potential flight delays",
            backstory="""You are an expert meteorologist with years of experience in aviation weather.
            You have access to real-time weather data and historical weather patterns to make informed
            predictions about potential flight delays.""",
            verbose=True,
        )
        super().__init__(config)

    async def check_weather(self, airport_code: str, date_time: str) -> Dict[str, Any]:
        """Check weather conditions for a specific airport at a given time."""
        # Instead of calling LLM, return mocked weather data
        weather_map = {
            "JFK": {"condition": "Clear", "temperature": "72°F", "wind": "5mph NE", "risk": "Low"},
            "LAX": {"condition": "Sunny", "temperature": "82°F", "wind": "8mph W", "risk": "Low"},
            "ORD": {"condition": "Overcast", "temperature": "65°F", "wind": "12mph NW", "risk": "Moderate"},
            "DFW": {"condition": "Thunderstorms", "temperature": "75°F", "wind": "20mph S", "risk": "High"},
            "ATL": {"condition": "Rain", "temperature": "70°F", "wind": "15mph SE", "risk": "Moderate"},
        }
        
        # Return default data for unknown airports
        weather_data = weather_map.get(airport_code.upper(), 
                                      {"condition": "Unknown", "temperature": "70°F", "wind": "10mph", "risk": "Unknown"})
        
        return {
            "airport": airport_code,
            "timestamp": date_time,
            "condition": weather_data["condition"],
            "temperature": weather_data["temperature"],
            "wind": weather_data["wind"],
            "delay_risk": weather_data["risk"],
            "summary": f"Weather at {airport_code} is {weather_data['condition']} with {weather_data['temperature']}. Wind: {weather_data['wind']}. Delay risk: {weather_data['risk']}."
        }
