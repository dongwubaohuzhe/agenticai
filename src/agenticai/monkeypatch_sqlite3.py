"""
Monkeypatch for SQLite3 to work with older versions.
"""

import importlib
import sys


def patch():
    """
    Patch sqlite3 for ChromaDB compatibility
    """
    print("Applying SQLite3 patch for ChromaDB...")

    # Import ChromaDB only after patching is set up
    try:
        # Check whether chromadb is already imported
        if "chromadb" in sys.modules:
            print("WARNING: ChromaDB already imported, patching may not work!")

        # Create a dummy function to replace the version check
        def dummy_function(*args, **kwargs):
            pass

        # Get the module and apply the patch
        chromadb_spec = importlib.util.find_spec("chromadb")
        if not chromadb_spec:
            print("ChromaDB module not found!")
            return False

        # Load the module
        chromadb = importlib.util.module_from_spec(chromadb_spec)

        # Monkey patch by replacing the function pointer
        if hasattr(chromadb, "__init__") and hasattr(chromadb.__init__, "_raise_old_sqlite_error"):
            chromadb.__init__._raise_old_sqlite_error = dummy_function
            print("SQLite3 version check bypassed.")
            return True
        else:
            print("Could not find the SQLite version check function to patch.")
            return False

    except Exception as e:
        print(f"Failed to apply SQLite3 patch: {e}")
        return False
