import json
import time
from typing import Any, Optional


class Memory:
    """Memory system for storing agent interactions and results.
    Uses a simple in-memory dictionary instead of ChromaDB to avoid SQLite issues.
    """

    def __init__(self, collection_name: str = "flight_delay_system"):
        """Initialize the simple memory system."""
        self.collection_name = collection_name
        self.documents = {}  # id -> document
        self.metadatas = {}  # id -> metadata
        print("Using simple in-memory storage instead of ChromaDB")

    def store(
        self, agent_name: str, task: str, result: dict[str, Any], metadata: Optional[dict[str, Any]] = None
    ) -> str:
        """Store an agent interaction in memory."""
        if metadata is None:
            metadata = {}

        # Create string-based metadata
        string_metadata = {k: str(v) for k, v in metadata.items()}
        string_metadata["agent"] = agent_name
        string_metadata["task"] = task
        string_metadata["timestamp"] = str(time.time())

        # Generate a unique ID
        doc_id = f"{agent_name}_{int(time.time())}_{len(self.documents) + 1}"

        # Store in memory
        self.documents[doc_id] = json.dumps(result)
        self.metadatas[doc_id] = string_metadata

        return doc_id

    def retrieve(self, query: str, n_results: int = 5) -> list[dict[str, Any]]:
        """Retrieve relevant memories based on a query.
        Note: Without ChromaDB, we don't have semantic search, so we just do basic keyword matching.
        """
        # Very simple keyword search
        matching_ids = []

        for doc_id, doc_text in self.documents.items():
            # Check if query appears in the document
            if query.lower() in doc_text.lower():
                matching_ids.append((doc_id, 1.0))  # Score 1.0 for matches

        # Sort by recency if no matches (fallback)
        if not matching_ids:
            # Sort documents by timestamp in metadata
            sorted_ids = sorted(
                self.metadatas.keys(), key=lambda doc_key: float(self.metadatas[doc_key].get("timestamp", "0")), reverse=True
            )
            matching_ids = [(doc_key, 0.5) for doc_key in sorted_ids[:n_results]]

        # Get top N results
        top_ids = [doc_key for doc_key, _ in matching_ids[:n_results]]

        # Format results
        documents = []
        for doc_id in top_ids:
            try:
                parsed_doc = json.loads(self.documents[doc_id])
                parsed_doc["metadata"] = self.metadatas[doc_id]
                documents.append(parsed_doc)
            except json.JSONDecodeError:
                # Skip documents that can't be parsed
                continue

        return documents

    def retrieve_by_agent(self, agent_name: str, n_results: int = 10) -> list[dict[str, Any]]:
        """Retrieve memories related to a specific agent."""
        return self._get_documents_by_metadata({"agent": agent_name}, n_results)

    def _get_documents_by_metadata(self, metadata_filter: dict[str, str], n_results: int = 10) -> list[dict[str, Any]]:
        """Get documents matching specific metadata filters."""
        matching_ids = []

        # Filter documents by metadata
        for doc_id, metadata in self.metadatas.items():
            matches = True
            for k, v in metadata_filter.items():
                if metadata.get(k) != v:
                    matches = False
                    break

            if matches:
                matching_ids.append(doc_id)

        # Sort by timestamp
        matching_ids = sorted(
            matching_ids, key=lambda doc_key: float(self.metadatas[doc_key].get("timestamp", "0")), reverse=True
        )

        # Get top N results
        top_ids = matching_ids[:n_results]

        # Format results
        documents = []
        for doc_id in top_ids:
            try:
                parsed_doc = json.loads(self.documents[doc_id])
                parsed_doc["metadata"] = self.metadatas[doc_id]
                documents.append(parsed_doc)
            except json.JSONDecodeError:
                # Skip documents that can't be parsed
                continue

        return documents
