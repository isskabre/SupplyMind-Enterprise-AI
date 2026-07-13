"""System-level API endpoints."""

from fastapi import APIRouter

from supplymind import __version__

router = APIRouter(tags=["System"])


@router.get("/health")
def health() -> dict[str, str]:
    """Return the current application health status."""
    return {
        "status": "healthy",
    }


@router.get("/version")
def version() -> dict[str, str]:
    """Return the current application version."""
    return {
        "version": __version__,
    }