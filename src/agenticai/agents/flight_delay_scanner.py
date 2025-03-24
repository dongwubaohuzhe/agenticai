from typing import Any, Dict

from .base import AgentConfig, BaseAgent


class FlightDelayScannerAgent(BaseAgent):
    """Agent responsible for scanning and analyzing potential flight delays."""

    def __init__(self):
        config = AgentConfig(
            name="FlightDelayScanner",
            role="Flight Delay Analysis Specialist",
            goal="Accurately assess flight delay risks and provide timely alerts",
            backstory="""You are an expert in flight operations with years of experience in the aviation industry.
            You have access to real-time flight data, historical delay patterns, and airport conditions to make
            accurate predictions about potential flight delays.""",
            verbose=True,
        )
        super().__init__(config)

    async def analyze_delay(self, flight_number: str, route: str, date: str) -> Dict[str, Any]:
        """Analyze delay probability for a specific flight."""
        # Instead of calling LLM, return mocked delay data
        # Create deterministic but varied responses based on flight number
        last_digit = int(flight_number[-1]) if flight_number[-1].isdigit() else 0
        
        delay_statuses = ["ON TIME", "SLIGHT DELAY", "DELAYED", "SIGNIFICANTLY DELAYED", "CANCELLED"]
        delay_reasons = [
            "No delays expected",
            "Minor air traffic congestion",
            "Weather conditions at destination",
            "Technical maintenance required",
            "Crew availability issues",
            "Airport capacity constraints",
            "Air traffic control restrictions",
            "Previous flight delay impact",
            "Incoming aircraft delayed",
            "Operational constraints"
        ]
        
        # Use the flight number to determine status (for demo purposes)
        status_index = last_digit % len(delay_statuses)
        reason_index = (last_digit * 2) % len(delay_reasons)
        
        delay_mins = last_digit * 15 if status_index > 0 else 0
        
        return {
            "flight_number": flight_number,
            "route": route,
            "date": date,
            "delay_status": delay_statuses[status_index],
            "delay_reason": delay_reasons[reason_index],
            "predicted_delay_minutes": delay_mins,
            "confidence": "90%",
            "recommendation": "Monitor flight status" if delay_mins < 30 else "Consider alternative arrangements"
        }
