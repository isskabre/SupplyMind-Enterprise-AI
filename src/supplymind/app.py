from fastapi import FastAPI

from supplymind import __version__
from supplymind.core.config import settings
from supplymind.core.logger import configure_logging

configure_logging()

app = FastAPI(
    title=settings.app_name,
    version=__version__,
    description="Enterprise AI platform for supply chain intelligence.",
)


@app.get("/")
def root() -> dict:
    return {
        "application": settings.app_name,
        "version": __version__,
        "status": "running",
    }

@app.get("/health")
def health() -> dict:
    return {
        "status": "healthy",
    }

@app.get("/version")
def version() -> dict:
    return {
        "version": __version__,
    }