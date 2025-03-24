from typing import Any, Dict, List

from .base import AgentConfig, BaseAgent


class TravelOrganizerAgent(BaseAgent):
    """Agent responsible for organizing travel documents and updates."""

    def __init__(self):
        config = AgentConfig(
            name="TravelOrganizer",
            role="Travel Documentation Specialist",
            goal="Organize and maintain all travel-related documents and status updates in a centralized system",
            backstory="""You are a meticulous document management specialist with expertise in organizing
            travel information. You excel at creating clear folder structures, naming conventions, and
            status tracking systems to ensure all travel information is easily accessible and up to date.""",
            verbose=True,
            allow_delegation=False,
        )
        super().__init__(config)

    async def organize_travel_documents(
        self,
        booking_details: Dict[str, Any],
        documents: List[Dict[str, Any]],
        status_updates: List[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Organize travel documents and updates in a structured folder system."""
        documents_str = ""
        for i, doc in enumerate(documents):
            documents_str += f"- Document {i + 1}: {doc.get('name')} ({doc.get('type')})\n"

        updates_str = ""
        if status_updates:
            updates_str = "\nStatus Updates:\n"
            for i, update in enumerate(status_updates):
                updates_str += f"- Update {i + 1}: {update.get('timestamp')} - {update.get('status')}\n"

        task = f"""Organize all travel documents and updates in a structured folder system:

        Booking details:
        - Traveler: {booking_details.get("traveler_name")}
        - Trip ID: {booking_details.get("trip_id")}
        - Dates: {booking_details.get("travel_dates")}
        - Destination: {booking_details.get("destination")}

        Documents to organize:
        {documents_str}
        {updates_str}

        Tasks:
        1. Design a logical folder structure for organizing all travel documents
        2. Create a naming convention for files to ensure easy identification
        3. Establish a status log format to track all changes and updates
        4. Develop a system for flagging important documents that need attention
        5. Create a summary document providing an overview of the trip status

        Provide a detailed plan for organizing all travel documents with folder structure and naming conventions."""

        context = {"booking_details": booking_details, "documents": documents, "status_updates": status_updates or []}

        return await self.execute(task, context)
