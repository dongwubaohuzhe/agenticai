from typing import Any, Dict, Optional

from .base import AgentConfig, BaseAgent


class ReservationAdjusterAgent(BaseAgent):
    """Agent responsible for adjusting hotel and transport reservations based on flight delays."""

    def __init__(self):
        config = AgentConfig(
            name="ReservationAdjuster",
            role="Travel Reservation Specialist",
            goal="Efficiently update hotel and transportation reservations to accommodate flight delays",
            backstory="""You are an experienced travel agent with deep knowledge of reservation systems.
            You have excellent relationships with hotels, car rental companies, and other travel providers,
            allowing you to quickly make changes to bookings when flight delays occur.""",
            verbose=True,
            allow_delegation=False,
        )
        super().__init__(config)

    async def adjust_reservations(
        self, booking_data: Dict[str, Any], delay_info: Dict[str, Any], new_arrival_time: Optional[str] = None
    ) -> Dict[str, Any]:
        """Adjust reservations based on flight delay information."""
        task = f"""Adjust travel reservations based on flight delay information:

        Original booking details:
        - Hotel check-in: {booking_data.get("hotel_check_in")}
        - Car rental pickup: {booking_data.get("car_rental_pickup")}
        - Other reservations: {booking_data.get("other_reservations", "None")}

        Flight delay details:
        - Flight: {delay_info.get("flight_number")}
        - Original arrival: {delay_info.get("original_arrival")}
        - Expected new arrival: {new_arrival_time or "To be determined"}
        - Delay reason: {delay_info.get("delay_reason", "Unknown")}

        Tasks:
        1. Analyze if reservations need adjustment based on delay information
        2. Determine specific changes needed for each reservation
        3. Draft communication to each provider (hotel, car rental, etc.)
        4. Identify any potential fees or penalties for changes
        5. Suggest alternatives if original reservations cannot be modified

        Provide a detailed plan for reservation adjustments with specific actions."""

        context = {"booking_data": booking_data, "delay_info": delay_info, "new_arrival_time": new_arrival_time}

        return await self.execute(task, context)
