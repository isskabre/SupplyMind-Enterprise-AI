"""System-level API endpoints."""

from fastapi import APIRouter

from supplymind import __version__
from supplymind.core.config import settings
from supplymind.api.schemas import (
    ApiResponse,
    HealthData,
    RootData,
    VersionData,
)

router = APIRouter(tags=["System"])


@router.get("/", response_model=ApiResponse[RootData])
def root() -> ApiResponse[RootData]:
    """Root endpoint."""

    return ApiResponse(
        message="Application is running.",
        data=RootData(
            application=settings.app_name,
            version=__version__,
            status="running",
        ),
    )


@router.get("/health", response_model=ApiResponse[HealthData])
def health() -> ApiResponse[HealthData]:
    """Health check."""

    return ApiResponse(
        message="Health check successful.",
        data=HealthData(
            status="healthy",
        ),
    )


@router.get("/version", response_model=ApiResponse[VersionData])
def version() -> ApiResponse[VersionData]:
    """Application version."""

    return ApiResponse(
        message="Version retrieved successfully.",
        data=VersionData(
            version=__version__,
        ),
    )