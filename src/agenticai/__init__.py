"""
Multi-Agent Flight Delay Response System

A multi-agent system that responds intelligently to flight delays by managing
weather checks, delay predictions, reservation adjustments, stakeholder
notifications, and alternate travel suggestions.
"""

from .agents import (
    AlternativeRouteSuggesterAgent,
    FlightDelayScannerAgent,
    ReservationAdjusterAgent,
    StakeholderNotifierAgent,
    TravelOrganizerAgent,
    WeatherCheckerAgent,
)
from .core import FlightDelayCrew, Monitoring
from .resources import FileSystem, FlightAPI, Memory, NotificationAPI, WeatherAPI

__version__ = "0.1.0"

from .api import app as api_app
from .run_api import run_server
from .run_app import run_app

__all__ = [
    "WeatherCheckerAgent",
    "FlightDelayScannerAgent",
    "ReservationAdjusterAgent",
    "StakeholderNotifierAgent",
    "AlternativeRouteSuggesterAgent",
    "TravelOrganizerAgent",
    "FlightDelayCrew",
    "Monitoring",
    "Memory",
    "FileSystem",
    "WeatherAPI",
    "FlightAPI",
    "NotificationAPI",
    "api_app",
    "run_server",
    "run_app",
]
