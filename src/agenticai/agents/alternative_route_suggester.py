from typing import Any, Dict

from .base import AgentConfig, BaseAgent


class AlternativeRouteSuggesterAgent(BaseAgent):
    """Agent responsible for suggesting alternative travel routes when flights are delayed."""

    def __init__(self):
        config = AgentConfig(
            name="AlternativeRouteSuggester",
            role="Travel Route Optimization Specialist",
            goal="Find the fastest and most convenient alternative travel options for delayed flights",
            backstory="""You are a travel logistics expert with extensive knowledge of flight routes,
            connections, and alternative transportation options. Your job is to help travelers quickly
            find alternative ways to reach their destination when faced with flight delays or cancellations.""",
            verbose=True,
        )
        super().__init__(config)

    async def suggest_alternatives(self, current_flight: Dict[str, Any], destination: str) -> Dict[str, Any]:
        """Suggest alternative routes to a destination when a flight is delayed."""
        # Generate simulated alternative routes
        origin = current_flight.get("origin", "Unknown")
        flight_num = current_flight.get("flight_number", "Unknown")
        
        # Create mocked alternative routes
        alternatives = []
        
        # Direct flight alternative (different airline)
        direct = {
            "type": "direct_flight",
            "flight": f"DL{int(flight_num[2:]) + 100}" if flight_num[0:2].isalpha() else "DL2532",
            "airline": "Delta Airlines",
            "departure_time": "2 hours from now",
            "arrival_time": "4 hours from now",
            "price_difference": "+$150",
            "availability": "6 seats left"
        }
        
        # Connection flight alternative
        connecting_cities = {
            "JFK": "BOS",
            "LAX": "SFO",
            "ORD": "DTW",
            "DFW": "IAH",
            "ATL": "CLT"
        }
        connection = connecting_cities.get(origin, "DCA")
        
        connection_flight = {
            "type": "connection",
            "flights": [
                {
                    "flight": f"UA{int(flight_num[2:]) - 50}" if flight_num[0:2].isalpha() else "UA1422",
                    "from": origin,
                    "to": connection,
                    "departure_time": "1.5 hours from now"
                },
                {
                    "flight": f"UA{int(flight_num[2:]) + 75}" if flight_num[0:2].isalpha() else "UA1575",
                    "from": connection,
                    "to": destination,
                    "departure_time": "4 hours from now"
                }
            ],
            "airline": "United Airlines",
            "total_travel_time": "6.5 hours",
            "price_difference": "+$50",
            "availability": "12 seats left"
        }
        
        # Alternative airport
        nearby_airports = {
            "JFK": "LGA",
            "LAX": "BUR",
            "ORD": "MDW",
            "DFW": "DAL",
            "ATL": "PDK"
        }
        alt_airport = nearby_airports.get(destination, destination)
        
        alternative_airport = {
            "type": "alternative_airport",
            "flight": f"AA{int(flight_num[2:]) + 200}" if flight_num[0:2].isalpha() else "AA3689",
            "airline": "American Airlines",
            "departure_time": "3 hours from now",
            "arrival_airport": alt_airport,
            "distance_to_original": "25 miles",
            "ground_transport": "Taxi, Shuttle, Rideshare available",
            "price_difference": "-$75",
            "availability": "2 seats left"
        }
        
        # Add all alternatives
        alternatives.extend([direct, connection_flight, alternative_airport])
        
        return {
            "original_flight": flight_num,
            "origin": origin,
            "destination": destination,
            "alternatives": alternatives,
            "recommendation": "We recommend the direct Delta flight as the fastest option to your destination."
        }
