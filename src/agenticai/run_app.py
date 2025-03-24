import os
import shutil
import subprocess
import threading
import time
import webbrowser
from pathlib import Path
from typing import Optional

from .run_api import run_server


def run_ui_server(api_port: int = 8000) -> Optional[subprocess.Popen]:
    """Run the UI server."""
    ui_dir = Path(__file__).parent.parent.parent / "ui"

    # Custom exception classes with meaningful names to avoid TRY003 issues
    class UIDirectoryNotFound(FileNotFoundError):
        """UI directory could not be found at the expected location."""
        pass

    class NPMNotFound(OSError):
        """npm executable not found in PATH."""
        pass

    # Verify ui directory exists
    if not ui_dir.exists() or not ui_dir.is_dir():
        raise UIDirectoryNotFound(str(ui_dir))

    # Check for npm executable - use absolute path from shutil.which
    npm_path = shutil.which("npm")
    if not npm_path:
        raise NPMNotFound()

    if not (ui_dir / "node_modules").exists():
        print("Installing UI dependencies...")
        try:
            # Use the full path to npm for security
            # We explicitly ignore bandit warnings here as we've verified the npm path
            subprocess.run(  # nosec B603, B607
                [npm_path, "install"],
                cwd=ui_dir,
                check=True,
                capture_output=True,
                text=True,
                env=os.environ.copy()
            )
        except subprocess.CalledProcessError as e:
            print(f"Error installing UI dependencies: {e}")
            raise

    # Run the UI server
    try:
        # Use the full path to npm for security
        # We explicitly ignore bandit warnings here as we've verified the npm path
        process = subprocess.Popen(  # nosec B603, B607
            [npm_path, "run", "dev"],
            cwd=ui_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=os.environ.copy()
        )

        # Open browser after a short delay
        def open_browser():
            try:
                time.sleep(2)
                webbrowser.open("http://localhost:3000")
            except Exception as e:
                print(f"Error opening browser: {e}")

        threading.Thread(target=open_browser).start()

        # Check if process started successfully
        time.sleep(1)
        if process.poll() is not None:
            print(f"UI server failed to start (exit code: {process.returncode})")
            return None
        else:
            return process
    except Exception as e:
        print(f"Error starting UI server: {e}")
        return None


def run_app():
    """Run both the API server and UI development server"""
    # Start the UI server in a separate process
    print("Starting UI development server...")
    try:
        ui_process = run_ui_server()
    except Exception as e:
        print(f"Failed to start UI server: {e}")
        ui_process = None

    # Open the browser after a short delay
    def open_browser():
        time.sleep(2)
        try:
            webbrowser.open("http://localhost:3000")
        except Exception as e:
            print(f"Could not open browser: {e}")

    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    try:
        # Start the API server in the current process
        print("Starting API server...")
        run_server()
    finally:
        # Terminate the UI process when the API server exits
        if ui_process:
            print("Shutting down UI server...")
            ui_process.terminate()
            try:
                ui_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                ui_process.kill()


if __name__ == "__main__":
    run_app()
