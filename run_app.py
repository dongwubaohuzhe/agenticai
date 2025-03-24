#!/usr/bin/env python
"""
Bootstrap script that mocks ChromaDB before importing any modules.
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

# Now import and run the API
try:
    from agenticai.run_api import run_server

    print("Starting the API server...")
    run_server()
except Exception as e:
    print(f"Error starting application: {e}")
    import traceback

    traceback.print_exc()
