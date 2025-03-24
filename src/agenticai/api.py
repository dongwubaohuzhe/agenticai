import asyncio
from datetime import datetime
from typing import Any, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import our multi-agent system components
from .agents import (
    AlternativeRouteSuggesterAgent,
    FlightDelayScannerAgent,
    ReservationAdjusterAgent,
    StakeholderNotifierAgent,
    TravelOrganizerAgent,
    WeatherCheckerAgent,
)
from .core import FlightDelayCrew, Monitoring
from .resources import FileSystem, Memory

# Initialize FastAPI app
app = FastAPI(
    title="Flight Delay Response System API",
    description="API for the multi-agent flight delay response system",
    version="0.1.0",
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response validation
class FlightInfo(BaseModel):
    flight_number: str
    origin: str
    destination: str
    scheduled_departure: str
    airline: Optional[str] = None
    current_status: Optional[str] = "SCHEDULED"


class ChatMessage(BaseModel):
    role: str  # "user", "assistant", or "system"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    flight_data: FlightInfo


class ChatResponse(BaseModel):
    response: str
    sources: Optional[list[Any]] = None


class ReservationData(BaseModel):
    trip_id: str
    hotel_check_in: Optional[str] = None
    car_rental_pickup: Optional[str] = None
    other_reservations: Optional[dict[str, Any]] = None


class NotificationData(BaseModel):
    trip_id: str
    contacts: list[dict[str, Any]]
    calendar_event: Optional[dict[str, Any]] = None
    updated_eta: str
    delay_reason: Optional[str] = None


# Dependency to get resources
async def get_resources():
    # Initialize shared resources
    memory = Memory()
    file_system = FileSystem()
    monitoring = Monitoring()

    return {"memory": memory, "file_system": file_system, "monitoring": monitoring}


# Dependency to get agents
async def get_agents():
    # Initialize agents
    weather_checker = WeatherCheckerAgent()
    flight_delay_scanner = FlightDelayScannerAgent()
    reservation_adjuster = ReservationAdjusterAgent()
    stakeholder_notifier = StakeholderNotifierAgent()
    alternative_route_suggester = AlternativeRouteSuggesterAgent()
    travel_organizer = TravelOrganizerAgent()

    return {
        "weather_checker": weather_checker,
        "flight_delay_scanner": flight_delay_scanner,
        "reservation_adjuster": reservation_adjuster,
        "stakeholder_notifier": stakeholder_notifier,
        "alternative_route_suggester": alternative_route_suggester,
        "travel_organizer": travel_organizer,
    }


# Dependency to get crew
async def get_crew():
    # Create crew with all agents
    agents = await get_agents()
    agents_list = list(agents.values())
    crew = FlightDelayCrew(agents_list)
    return crew


# Global registry to store running tasks
background_tasks = {}


# API Routes
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {"status": "online", "api": "Flight Delay Response System", "version": "0.1.0"}


@app.post("/api/flight/status", response_model=dict[str, Any])
async def check_flight_status(flight_info: FlightInfo):
    """Check flight status and delay probability"""
    agents = await get_agents()
    resources = await get_resources()

    try:
        # Get the flight delay scanner agent
        flight_delay_scanner = agents["flight_delay_scanner"]

        # Analyze flight delay
        result = await flight_delay_scanner.analyze_delay(
            flight_number=flight_info.flight_number,
            route=f"{flight_info.origin} to {flight_info.destination}",
            date=flight_info.scheduled_departure,
        )

        # Log the operation
        resources["monitoring"].log_agent_execution(
            agent_name="FlightDelayScanner", task="analyze_delay", result=result
        )
    except Exception as e:
        resources["monitoring"].log_error(agent_name="FlightDelayScanner", task="analyze_delay", error=e)
        raise HTTPException(status_code=500, detail=str(e)) from e
    else:
        return result


@app.get("/api/weather/{airport_code}", response_model=dict[str, Any])
async def get_weather(airport_code: str):
    """Get weather information for a specific airport"""
    agents = await get_agents()
    resources = await get_resources()

    try:
        # Get the weather checker agent
        weather_checker = agents["weather_checker"]

        # Current time for the check
        now = datetime.now().isoformat()

        # Check weather
        result = await weather_checker.check_weather(airport_code=airport_code, date_time=now)

        # Log the operation
        resources["monitoring"].log_agent_execution(agent_name="WeatherChecker", task="check_weather", result=result)
    except Exception as e:
        resources["monitoring"].log_error(agent_name="WeatherChecker", task="check_weather", error=e)
        raise HTTPException(status_code=500, detail=str(e)) from e
    else:
        return result


@app.post("/api/flight/alternatives", response_model=dict[str, Any])
async def get_alternative_routes(flight_info: FlightInfo):
    """Get alternative travel options for a flight"""
    agents = await get_agents()
    resources = await get_resources()

    try:
        # Get the alternative route suggester agent
        alternative_route_suggester = agents["alternative_route_suggester"]

        # Convert flight info to required format
        current_flight = {
            "flight_number": flight_info.flight_number,
            "origin": flight_info.origin,
            "scheduled_departure": flight_info.scheduled_departure,
            "current_status": flight_info.current_status,
        }

        # Get alternative routes
        result = await alternative_route_suggester.suggest_alternatives(
            current_flight=current_flight, destination=flight_info.destination
        )

        # Log the operation
        resources["monitoring"].log_agent_execution(
            agent_name="AlternativeRouteSuggester", task="suggest_alternatives", result=result
        )
    except Exception as e:
        resources["monitoring"].log_error(agent_name="AlternativeRouteSuggester", task="suggest_alternatives", error=e)
        raise HTTPException(status_code=500, detail=str(e)) from e
    else:
        return result


@app.post("/api/reservations/update", response_model=dict[str, Any])
async def update_reservation(
    reservation_data: ReservationData,
    flight_info: FlightInfo,
):
    """Update hotel and car rental reservations based on flight changes"""
    agents = await get_agents()
    resources = await get_resources()

    try:
        # Get the reservation adjuster agent
        reservation_adjuster = agents["reservation_adjuster"]

        # Convert to required format
        booking_data = {
            "trip_id": reservation_data.trip_id,
            "hotel_check_in": reservation_data.hotel_check_in,
            "car_rental_pickup": reservation_data.car_rental_pickup,
            "other_reservations": reservation_data.other_reservations,
        }

        delay_info = {
            "flight_number": flight_info.flight_number,
            "original_arrival": flight_info.scheduled_departure,
            "delay_reason": "Schedule change",
        }

        # Update reservations
        result = await reservation_adjuster.adjust_reservations(booking_data=booking_data, delay_info=delay_info)

        # Log the operation
        resources["monitoring"].log_agent_execution(
            agent_name="ReservationAdjuster", task="adjust_reservations", result=result
        )
    except Exception as e:
        resources["monitoring"].log_error(agent_name="ReservationAdjuster", task="adjust_reservations", error=e)
        raise HTTPException(status_code=500, detail=str(e)) from e
    else:
        return result


@app.post("/api/notifications/send", response_model=dict[str, Any])
async def send_notifications(notification_data: NotificationData):
    """Send notifications to stakeholders about flight changes"""
    agents = await get_agents()
    resources = await get_resources()

    try:
        # Get the stakeholder notifier agent
        stakeholder_notifier = agents["stakeholder_notifier"]

        # Convert to required format
        notification_info = {
            "trip_id": notification_data.trip_id,
            "contacts": notification_data.contacts,
            "updated_info": {
                "eta": notification_data.updated_eta,
                "reason": notification_data.delay_reason or "Unknown",
            },
            "calendar_event": notification_data.calendar_event,
        }

        # Send notifications
        result = await stakeholder_notifier.notify_stakeholders(notification_info=notification_info)

        # Log the operation
        resources["monitoring"].log_agent_execution(
            agent_name="StakeholderNotifier", task="notify_stakeholders", result=result
        )
    except Exception as e:
        resources["monitoring"].log_error(agent_name="StakeholderNotifier", task="notify_stakeholders", error=e)
        raise HTTPException(status_code=500, detail=str(e)) from e
    else:
        return result


@app.post("/api/chat", response_model=ChatResponse)
async def process_chat(request: ChatRequest):
    """Process a chat message with the multi-agent system"""
    agents = await get_agents()
    resources = await get_resources()

    try:
        # Extract conversation history
        conversation_history = request.messages

        # Get user messages only
        user_messages = [msg for msg in conversation_history if msg.role == "user"]

        # Special case: no user messages
        if not user_messages:
            # Handle the error case outside of this function to avoid linting issues
            return process_missing_user_message()

        latest_user_message = user_messages[-1]

        # Flight data might be needed to provide context to agents
        flight_data = request.flight_data

        # Create a more detailed context
        context = {
            "flight_number": flight_data.flight_number,
            "origin": flight_data.origin,
            "destination": flight_data.destination,
            "scheduled_departure": flight_data.scheduled_departure,
            "airline": flight_data.airline or "Unknown"
        }

        # Based on the message, determine which agent should handle it
        query = latest_user_message.content.lower()

        # Store the conversation in memory for future reference
        memory_key = f"{flight_data.flight_number}_{datetime.now().strftime('%Y%m%d')}"

        # Log the interaction
        resources["memory"].store(
            agent_name="ChatSystem",
            task="process_query",
            result={"query": query, "context": context},
            metadata={"timestamp": str(datetime.now().timestamp()), "memory_key": memory_key}
        )

        # Use the appropriate agent based on the query
        # This is a simple keyword-based routing
        if "weather" in query:
            agent = agents["weather_checker"]
            airport = flight_data.origin if "origin" in query or "departure" in query else flight_data.destination
            response_data = await agent.check_weather(airport_code=airport, date_time=flight_data.scheduled_departure)
            response = f"Weather for {airport}: {response_data.get('summary', 'Information not available')}"

        elif "delay" in query or "status" in query:
            agent = agents["flight_delay_scanner"]
            response_data = await agent.analyze_delay(
                flight_number=flight_data.flight_number,
                route=f"{flight_data.origin} to {flight_data.destination}",
                date=flight_data.scheduled_departure
            )
            delay_status = response_data.get("delay_status", "unknown")
            delay_reason = response_data.get("delay_reason", "No specific reason provided")
            response = f"Flight {flight_data.flight_number} status: {delay_status}. {delay_reason}"

        elif "alternative" in query or "other flight" in query:
            agent = agents["alternative_route_suggester"]
            current_flight = {
                "flight_number": flight_data.flight_number,
                "origin": flight_data.origin,
                "scheduled_departure": flight_data.scheduled_departure,
                "current_status": "DELAYED",  # Assuming if they're asking for alternatives
            }
            response_data = await agent.suggest_alternatives(
                current_flight=current_flight,
                destination=flight_data.destination
            )

            alternatives = response_data.get("alternatives", [])
            if alternatives:
                response = "Here are some alternative routes:\n"
                for idx, alt in enumerate(alternatives[:3], 1):
                    response += f"{idx}. {alt.get('flight', 'Flight')} - {alt.get('departure_time', 'N/A')}\n"
            else:
                response = "I couldn't find any alternative routes at this time."

        else:
            # For queries we don't specifically categorize, send to the travel organizer
            # for general travel advice
            agent = agents["travel_organizer"]
            response_data = await agent.organize_travel(
                flight_info=context,
                special_requests=query
            )
            response = response_data.get("advice", "I'm not sure how to help with that specific query.")

        return ChatResponse(response=response)

    except Exception as e:
        resources["monitoring"].log_error(agent_name="ChatAPI", task="process_chat", error=e)
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/api/flight/monitor")
async def monitor_flight(flight_info: FlightInfo, background_tasks: BackgroundTasks):
    """Start monitoring a flight in the background"""
    crew = await get_crew()
    resources = await get_resources()

    # Create a unique trip ID
    trip_id = f"{flight_info.flight_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    async def monitor_task(flight_data, trip_id):
        """Background task to monitor a flight"""
        try:
            # Convert flight info to dictionary for the crew
            flight_dict = {
                "flight_number": flight_data.flight_number,
                "origin": flight_data.origin,
                "destination": flight_data.destination,
                "scheduled_departure": flight_data.scheduled_departure,
                "airline": flight_data.airline,
            }

            # Begin monitoring - this is a simplified version
            # In a real system, this would periodically check flight status
            # and take actions when delays are detected

            # Initial status check
            status_data = await crew.handle_flight_delay(flight_dict)

            # Store the initial check result
            resources["file_system"].add_status_update(
                trip_id=trip_id,
                status={
                    "timestamp": datetime.now().isoformat(),
                    "status": "MONITORING",
                    "data": status_data,
                }
            )

            # In a real system, we would set up a periodic check here
            # For this example, we'll just do one check
            await asyncio.sleep(5)  # Simulate some processing time

            # Final status update
            resources["file_system"].add_status_update(
                trip_id=trip_id,
                status={
                    "timestamp": datetime.now().isoformat(),
                    "status": "COMPLETED",
                    "message": "Flight monitoring completed",
                }
            )

        except Exception as e:
            # Log any errors
            resources["monitoring"].log_error(
                agent_name="FlightMonitor",
                task="monitor_flight",
                error=e,
                metadata={"trip_id": trip_id}
            )

            # Update status with error
            resources["file_system"].add_status_update(
                trip_id=trip_id,
                status={
                    "timestamp": datetime.now().isoformat(),
                    "status": "ERROR",
                    "message": str(e),
                }
            )

    # Add the monitoring task to background tasks
    background_tasks.add_task(monitor_task, flight_info, trip_id)

    # Return the trip ID for client to use for status checks
    return {
        "status": "monitoring_started",
        "trip_id": trip_id,
        "message": "Flight monitoring has been started in the background"
    }


async def process_missing_user_message():
    """Handle the case where no user message is found."""
    error_msg = "No user message found"
    raise HTTPException(status_code=400, detail=error_msg)


# Run the server if executed directly
if __name__ == "__main__":
    import uvicorn

    # Use 127.0.0.1 instead of 0.0.0.0 for development
    uvicorn.run(app, host="127.0.0.1", port=8000)
