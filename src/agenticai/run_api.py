import uvicorn

from .config.settings import settings


def run_server():
    """Run the FastAPI server with uvicorn"""
    # Use 127.0.0.1 for development (localhost only) and host specified in settings for prod
    host = "127.0.0.1" if settings.ENV == "development" else settings.get("HOST", "127.0.0.1")
    uvicorn.run("agenticai.api:app", host=host, port=8000, reload=settings.ENV == "development")


if __name__ == "__main__":
    run_server()
