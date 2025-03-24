"""
Main entry point for the application with mock ChromaDB.
"""

import os
import sys

# Add the root directory to the path so we can import our mock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Import our mock first to ensure it's loaded before any actual chromadb import happens

# Set a temporary directory if disk space is low
if not os.path.exists("tmp"):
    os.makedirs("tmp", exist_ok=True)
os.environ["TMPDIR"] = os.path.abspath("tmp")

# Then import and run the API
from agenticai.api import run_server

if __name__ == "__main__":
    run_server()
