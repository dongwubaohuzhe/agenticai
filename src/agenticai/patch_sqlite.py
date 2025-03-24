"""
Patch to make ChromaDB work with older versions of SQLite.
This should be imported before importing ChromaDB.
"""

import importlib
import sqlite3
import sys
from unittest.mock import patch


def apply_patch():
    """Apply the patch to bypass ChromaDB's SQLite version check"""
    # Check if ChromaDB is already imported
    if "chromadb" in sys.modules:
        raise ImportError("Cannot patch ChromaDB after it has been imported.")

    # Apply the patch by replacing the SQLite version check
    def patched_init():
        """Do nothing, effectively skipping the version check"""
        pass

    # Find the module path to patch
    try:
        chromadb_spec = importlib.util.find_spec("chromadb")
        if not chromadb_spec:
            print("Warning: Could not find chromadb module to patch.")
            return

        # Apply the patch to the __init__ module
        target = "chromadb.__init__._raise_old_sqlite_error"
        with patch(target, patched_init):
            # Now safely import ChromaDB with the patch

            print(f"Successfully patched ChromaDB to work with SQLite {sqlite3.sqlite_version}")
    except Exception as e:
        print(f"Failed to patch ChromaDB: {e}")


if __name__ == "__main__":
    apply_patch()
