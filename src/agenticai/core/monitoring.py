import logging
import time
from typing import Any, Dict, Optional

from ..config.settings import settings

logger = logging.getLogger(__name__)


class Monitoring:
    """Simple monitoring system."""

    def __init__(self):
        """Initialize the monitoring system."""
        self.enabled = settings.ENABLE_MONITORING
        self.client = None

        if self.enabled:
            logger.info("Monitoring enabled")

    def log_agent_execution(
        self, agent_name: str, task: str, result: Any, metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log an agent execution."""
        if not self.enabled:
            logger.debug(f"Monitoring disabled, not logging agent execution: {agent_name}")
            return

        try:
            # Convert result to string if it's not a primitive type
            if isinstance(result, (dict, list)):
                import json

                result_str = json.dumps(result)
            else:
                result_str = str(result)

            # Prepare metadata
            meta = {"agent": agent_name, "task": task, "timestamp": time.time()}
            if metadata:
                meta.update(metadata)

            # Log to console in development
            logger.info(f"Agent execution: {agent_name} - {task}")
            logger.debug(f"Result: {result_str[:200]}...")
            logger.debug(f"Metadata: {meta}")

        except Exception as e:
            logger.error(f"Failed to log agent execution: {e}")

    def log_error(
        self, agent_name: str, task: str, error: Exception, metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log an error."""
        if not self.enabled:
            logger.debug(f"Monitoring disabled, not logging error: {agent_name}")
            return

        try:
            # Prepare metadata
            meta = {"agent": agent_name, "task": task, "error_type": type(error).__name__, "timestamp": time.time()}
            if metadata:
                meta.update(metadata)

            # Log to console
            logger.error(f"Error in agent {agent_name} - {task}: {error}")
            logger.debug(f"Error metadata: {meta}")

        except Exception as e:
            logger.error(f"Failed to log error: {e}")

    def start_trace(self, trace_id: str, name: str) -> None:
        """Start a trace for a sequence of agent operations."""
        if self.enabled:
            logger.info(f"Starting trace {trace_id}: {name}")

    def end_trace(self, trace_id: str) -> None:
        """End a trace for a sequence of agent operations."""
        if self.enabled:
            logger.info(f"Ending trace {trace_id}")
