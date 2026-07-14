"""System-level API endpoints."""

from fastapi import APIRouter, Depends

from supplymind.api.schemas import (
    ApiResponse,
    HealthData,
    RootData,
    VersionData,
)
from supplymind.core.dependencies import get_system_service
from supplymind.services.system_service import SystemService

router = APIRouter(tags=["System"])


@router.get("/", response_model=ApiResponse[RootData])
def root(
    service: SystemService = Depends(get_system_service),
) -> ApiResponse[RootData]:
    """Return versioned API information."""

    return ApiResponse[RootData](
        message="Application information retrieved successfully.",
        data=RootData(**service.get_root()),
    )


@router.get("/health", response_model=ApiResponse[HealthData])
def health(
    service: SystemService = Depends(get_system_service),
) -> ApiResponse[HealthData]:
    """Return application health information."""

    return ApiResponse[HealthData](
        message="Health check successful.",
        data=HealthData(**service.get_health()),
    )


@router.get("/version", response_model=ApiResponse[VersionData])
def version(
    service: SystemService = Depends(get_system_service),
) -> ApiResponse[VersionData]:
    """Return the current application version."""

    return ApiResponse[VersionData](
        message="Version retrieved successfully.",
        data=VersionData(**service.get_version()),
    )