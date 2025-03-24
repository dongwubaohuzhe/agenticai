#!/usr/bin/env python
"""
Simple server script that directly runs with uvicorn
"""

import importlib.util
import os
import sys

# Add the project root to sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Execute the mock_chromadb.py file to install the mock before any imports
mock_path = os.path.join(project_root, "mock_chromadb.py")
spec = importlib.util.spec_from_file_location("mock_chromadb", mock_path)
mock_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mock_module)

# Set a temporary directory
tmp_dir = os.path.join(project_root, "tmp")
os.makedirs(tmp_dir, exist_ok=True)
os.environ["TMPDIR"] = tmp_dir

# Import necessary modules
import uvicorn

# Run the server directly
if __name__ == "__main__":
    print("Starting the API server directly...")
    uvicorn.run(
        "agenticai.api:app",
        host="0.0.0.0",
        port=8080,  # Using port 8080 which is often exposed in containers
        reload=False,  # Disable reload to avoid forking issues
    )
