import asyncio
import logging

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Import agents
from .agents import (
    AlternativeRouteSuggesterAgent,
    FlightDelayScannerAgent,
    ReservationAdjusterAgent,
    StakeholderNotifierAgent,
    TravelOrganizerAgent,
    WeatherCheckerAgent,
)

# Import core components
from .core import FlightDelayCrew, Monitoring

# Import resources
from .resources import FileSystem, Memory


async def main():
    """Main application entry point."""
    logger.info("Starting Flight Delay Response System")

    # Initialize resources
    memory = Memory()
    file_system = FileSystem()
    monitoring = Monitoring()

    # Initialize agents
    weather_checker = WeatherCheckerAgent()
    flight_delay_scanner = FlightDelayScannerAgent()
    reservation_adjuster = ReservationAdjusterAgent()
    stakeholder_notifier = StakeholderNotifierAgent()
    alternative_route_suggester = AlternativeRouteSuggesterAgent()
    travel_organizer = TravelOrganizerAgent()

    # Create crew with all agents
    agents = [
        weather_checker,
        flight_delay_scanner,
        reservation_adjuster,
        stakeholder_notifier,
        alternative_route_suggester,
        travel_organizer,
    ]
    crew = FlightDelayCrew(agents)

    # Example flight delay scenario
    flight_info = {
        "flight_number": "AA123",
        "origin": "JFK",
        "destination": "LAX",
        "scheduled_departure": "2024-03-24T10:00:00Z",
        "current_status": "DELAYED",
        "delay_info": {"expected_delay": "2 hours", "reason": "Weather"},
    }

    # Example booking data
    booking_data = {
        "trip_id": "TRIP123456",
        "traveler_name": "John Doe",
        "travel_dates": "2024-03-24 to 2024-03-31",
        "hotel_check_in": "2024-03-24T16:00:00Z",
        "car_rental_pickup": "2024-03-24T17:00:00Z",
        "destination": "Los Angeles, CA",
    }

    # Create trip folder for documents
    file_system.create_trip_folder(booking_data["trip_id"])

    # Add initial flight information
    file_system.save_document(
        trip_id=booking_data["trip_id"], document_type="flight", content=flight_info, filename="flight_info.json"
    )

    # Add initial status
    file_system.add_status_update(
        trip_id=booking_data["trip_id"],
        status={
            "status": "Flight delayed",
            "timestamp": "2024-03-24T08:00:00Z",
            "details": "Flight AA123 delayed due to weather conditions.",
        },
    )

    try:
        # Start a monitoring trace
        trace_id = f"flight_delay_{flight_info['flight_number']}"
        monitoring.start_trace(trace_id, "Flight Delay Response")

        # Handle the flight delay
        logger.info(f"Handling delay for flight {flight_info['flight_number']}")
        result = await crew.handle_flight_delay(flight_info)

        # Log the result
        monitoring.log_agent_execution("FlightDelayCrew", "handle_flight_delay", result)

        # End the monitoring trace
        monitoring.end_trace(trace_id)

        logger.info("Flight delay handled successfully")
        logger.info(f"Result: {result}")

    except Exception as e:
        logger.error(f"Error handling flight delay: {e}")
        monitoring.log_error("FlightDelayCrew", "handle_flight_delay", e)


if __name__ == "__main__":
    asyncio.run(main())
