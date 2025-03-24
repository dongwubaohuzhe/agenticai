import json
import os
from datetime import datetime
from typing import Any, Optional


class FileSystem:
    """File system handler for document management."""

    def __init__(self, base_dir: str = "./data/travel_docs"):
        """Initialize the file system handler."""
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def create_trip_folder(self, trip_id: str) -> str:
        """Create a folder structure for a trip."""
        trip_dir = os.path.join(self.base_dir, trip_id)

        # Create main trip directory
        os.makedirs(trip_dir, exist_ok=True)

        # Create subdirectories
        subdirs = [
            "flight_info",
            "hotel_reservations",
            "car_rentals",
            "status_updates",
            "alternative_options",
            "notifications",
        ]

        for subdir in subdirs:
            os.makedirs(os.path.join(trip_dir, subdir), exist_ok=True)

        return trip_dir

    def save_document(
        self, trip_id: str, document_type: str, content: dict[str, Any], filename: Optional[str] = None
    ) -> str:
        """Save a document to the trip folder."""
        # Ensure trip folder exists
        trip_dir = os.path.join(self.base_dir, trip_id)
        if not os.path.exists(trip_dir):
            self.create_trip_folder(trip_id)

        # Determine the appropriate subdirectory
        if document_type in ["flight", "boarding_pass"]:
            subdir = "flight_info"
        elif document_type in ["hotel", "accommodation"]:
            subdir = "hotel_reservations"
        elif document_type in ["car", "rental"]:
            subdir = "car_rentals"
        elif document_type in ["status", "update"]:
            subdir = "status_updates"
        elif document_type in ["alternative", "option"]:
            subdir = "alternative_options"
        elif document_type in ["notification", "message"]:
            subdir = "notifications"
        else:
            subdir = ""  # Root of trip directory

        # Create the target directory path
        target_dir = os.path.join(trip_dir, subdir)
        os.makedirs(target_dir, exist_ok=True)

        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{document_type}_{timestamp}.json"

        # Ensure filename has .json extension
        if not filename.endswith(".json"):
            filename += ".json"

        # Full path to the file
        file_path = os.path.join(target_dir, filename)

        # Save the content as JSON
        with open(file_path, "w") as f:
            json.dump(content, f, indent=2)

        return file_path

    def add_status_update(self, trip_id: str, status: dict[str, Any]) -> str:
        """Add a status update to the trip folder."""
        # Ensure status has a timestamp
        if "timestamp" not in status:
            status["timestamp"] = datetime.now().isoformat()

        # Get existing status updates
        status_updates = self.get_status_updates(trip_id)
        status_updates.append(status)

        # Save the updated status list
        return self.save_document(
            trip_id=trip_id, document_type="status", content={"updates": status_updates}, filename="status_log.json"
        )

    def get_status_updates(self, trip_id: str) -> list[dict[str, Any]]:
        """Get all status updates for a trip."""
        status_file = os.path.join(self.base_dir, trip_id, "status_updates", "status_log.json")
        if os.path.exists(status_file):
            with open(status_file) as f:
                try:
                    data = json.load(f)
                    return data.get("updates", [])
                except json.JSONDecodeError:
                    return []
        return []

    def list_documents(self, trip_id: str, document_type: Optional[str] = None) -> list[str]:
        """List all documents for a trip."""
        trip_dir = os.path.join(self.base_dir, trip_id)

        if not os.path.exists(trip_dir):
            return []

        # Helper function to filter documents by type
        def filter_by_document_type(files: list[str]) -> list[str]:
            if not document_type:
                return files

            return [f for f in files if f.startswith(f"{document_type}_")]

        # Helper function to get all document files
        def get_document_files() -> list[str]:
            try:
                return [
                    f for f in os.listdir(trip_dir)
                    if os.path.isfile(os.path.join(trip_dir, f)) and not f.startswith(".")
                ]
            except Exception:
                return []

        document_files = get_document_files()
        return filter_by_document_type(document_files)
