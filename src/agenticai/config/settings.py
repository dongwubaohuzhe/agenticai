import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Settings
    API_TITLE: str = "Flight Delay Response System API"
    API_VERSION: str = "0.1.0"
    API_DEBUG: bool = True

    # Environment
    ENV: str = os.getenv("ENVIRONMENT", "development")

    # CORS
    CORS_ORIGINS: list[str] = ["*"]

    # File Storage
    STORAGE_PATH: str = os.getenv("STORAGE_PATH", str(Path.home() / ".flight_delay_system"))

    # Credentials (these would come from env variables in production)
    WEATHER_API_KEY: Optional[str] = os.getenv("WEATHER_API_KEY", "demo_key")
    FLIGHT_API_KEY: Optional[str] = os.getenv("FLIGHT_API_KEY", "demo_key")
    NOTIFICATION_API_KEY: Optional[str] = os.getenv("NOTIFICATION_API_KEY", "demo_key")

    # Database
    DB_CONNECTION_STRING: Optional[str] = os.getenv("DB_CONNECTION_STRING", "")

    # Monitoring
    ENABLE_MONITORING: bool = True
    LOGGING_LEVEL: str = os.getenv("LOGGING_LEVEL", "INFO")

    # Memory settings
    MEMORY_COLLECTION_NAME: str = "flight_delay_interactions"
    MEMORY_PERSIST_DIRECTORY: str = os.getenv("MEMORY_PERSIST_DIR", str(Path.home() / ".flight_delay_memory"))

    class Config:
        case_sensitive = True
        env_file = ".env"


# Create a global instance
settings = Settings()

# If we're in development mode, create storage directories if they don't exist
if settings.ENV == "development":
    os.makedirs(settings.STORAGE_PATH, exist_ok=True)
    os.makedirs(settings.MEMORY_PERSIST_DIRECTORY, exist_ok=True)
