from fastapi import FastAPI

from supplymind import __version__
from supplymind.api.router import api_router
from supplymind.core.config import settings
from supplymind.core.logger import configure_logging

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=__version__,
    description="Enterprise AI platform for supply chain intelligence.",
)

app.include_router(api_router)


@app.get("/", tags=["Application"])
def root() -> dict[str, str]:
    """Return basic application information."""
    return {
        "application": settings.app_name,
        "version": __version__,
        "status": "running",
    }